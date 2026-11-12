"""Did the last run of nb_kurs really update orders_by_region?

    python3 checks/check_orders.py

PASS only if all three hold:
  (1) the last run of nb_kurs has status Completed
  (2) orders_by_region has a Delta commit after that run started (60 s clock tolerance)
  (3) through the SQL endpoint, orders and amount per region in orders_by_region equal a GROUP BY over orders
      (amounts within 0.01), and the total is 1000 orders
Expected values come from the input (orders), never from the output. Prints one line per check, then PASS or FAIL;
exit 1 on FAIL. Reads only: never runs the notebook.

Locally the endpoint is a SQLite file and always in sync. Against Fabric, retry (3) for a few minutes when (2)
passes and (3) doesn't, because the SQL analytics endpoint syncs in the background.
"""
import datetime
import email.utils
import os
import pathlib
import re
import shutil
import sqlite3
import subprocess
import sys

WORKSPACE, LAKEHOUSE, NOTEBOOK = "tta210-lab", "lh_kurs", "nb_kurs"
DELTA_LOG = f"{WORKSPACE}.Workspace/{LAKEHOUSE}.Lakehouse/Tables/orders_by_region/_delta_log"
TOLERANCE = datetime.timedelta(seconds=60)
TOTAL_ORDERS = 1000


def fab(*args):
    exe = shutil.which("fab")
    if not exe:
        raise RuntimeError("fab not on PATH (source env.sh)")
    r = subprocess.run([exe, *args], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr.strip()


def rows(table_text):
    """Parse a fab table: header, dashes, rows; columns are separated by two or more spaces."""
    lines = [l for l in table_text.splitlines() if l.strip() and not set(l.strip()) <= {"-"}]
    if not lines:
        return []
    header = re.split(r"\s{2,}", lines[0].strip())
    return [dict(zip(header, re.split(r"\s{2,}", l.strip()))) for l in lines[1:]]


def utc(text):
    """2026-11-09T13:17:40.6980625 (seven digits, no zone) -> aware UTC datetime."""
    text = re.sub(r"(\.\d{6})\d+", r"\1", text.rstrip("Z"))
    return datetime.datetime.fromisoformat(text).replace(tzinfo=datetime.timezone.utc)


def last_run():
    code, out, err = fab("job", "run-list", f"{WORKSPACE}.Workspace/{NOTEBOOK}.Notebook")
    if code:
        return False, f"fab job run-list failed: {err}", None
    runs = rows(out)
    if not runs:
        return False, "no runs of nb_kurs", None
    run = max(runs, key=lambda r: utc(r["startTimeUtc"]))
    start = utc(run["startTimeUtc"])
    ok = run["status"] == "Completed"
    return ok, f"last run {run['id']} status {run['status']}, started {start:%Y-%m-%d %H:%M:%S} UTC", start


def commit_after(start):
    code, out, err = fab("ls", "-l", DELTA_LOG)
    if code:
        return False, f"no Delta log for orders_by_region ({err})"
    times = [email.utils.parsedate_to_datetime(r["lastModified"]) for r in rows(out) if r.get("name", "").endswith(".json")]
    if not times:
        return False, "Delta log has no commits"
    newest = max(times)
    if start is None:
        return False, f"newest commit {newest:%H:%M:%S} UTC, no run to compare with"
    ok = newest >= start - TOLERANCE
    word = "after" if ok else "before"
    return ok, f"newest commit {newest:%H:%M:%S} UTC is {word} the run started ({start:%H:%M:%S} UTC)"


def rows_match():
    state = os.environ.get("VERIFY_STATE")
    if not state:
        return False, "VERIFY_STATE not set (source env.sh)"
    db = pathlib.Path(state) / "endpoint.db"
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        expected = {r: (n, a) for r, n, a in con.execute(
            "SELECT region, COUNT(*), SUM(amount) FROM orders GROUP BY region")}
        actual = {r: (n, a) for r, n, a in con.execute("SELECT region, orders, amount FROM orders_by_region")}
    except sqlite3.Error as e:
        return False, f"SQL endpoint: {e}"
    problems = []
    for region in sorted(set(expected) | set(actual)):
        e, a = expected.get(region), actual.get(region)
        if e is None or a is None:
            problems.append(f"{region} {'missing' if a is None else 'not in orders'}")
        elif e[0] != a[0] or abs(e[1] - a[1]) > 0.01:
            problems.append(f"{region} {a[0]}/{a[1]:.2f}, expected {e[0]}/{e[1]:.2f}")
    total = sum(n for n, _ in actual.values())
    if total != TOTAL_ORDERS:
        problems.append(f"total {total} orders, expected {TOTAL_ORDERS}")
    if problems:
        return False, "orders_by_region: " + "; ".join(problems)
    return True, f"{len(actual)} regions, {total} orders, amounts equal GROUP BY over orders"


def main():
    results = []
    ok1, msg1, start = last_run()
    results.append((ok1, "(1) " + msg1))
    ok2, msg2 = commit_after(start)
    results.append((ok2, "(2) " + msg2))
    ok3, msg3 = rows_match()
    results.append((ok3, "(3) " + msg3))
    for ok, msg in results:
        print(f"{'PASS' if ok else 'FAIL'} {msg}")
    passed = all(ok for ok, _ in results)
    print("PASS" if passed else "FAIL")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
