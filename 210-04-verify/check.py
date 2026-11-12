"""Check your verification script for exercise 210-04.

    python3 check.py <project folder>

Runs <project>/checks/check_orders.py once per state (empty, canceled, done), with the fake fab on the PATH and
VERIFY_STATE pointing at a fresh copy of the state under a neutral name. Expects FAIL, FAIL, PASS: exactly one PASS.
A state counts as PASS when the script exits 0 and its last line is PASS, and as FAIL when it exits 1 and its last
line is FAIL; a crash counts as neither.

One more run checks that the expected values come from the input: a copy of done in which one order in `orders`
costs 1.00 more. orders_by_region no longer matches a GROUP BY over orders, so the right answer is FAIL.
"""
import os
import pathlib
import shutil
import sqlite3
import subprocess
import sys
import tempfile

here = pathlib.Path(__file__).resolve().parent
project = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "project").resolve()
script = project / "checks" / "check_orders.py"
TIMEOUT = 30
ok = True


def say(good, label, why=""):
    global ok
    ok &= good
    print(f"{'ok  ' if good else 'FAIL'}  {label}" + ("" if good or not why else f": {why}"))


def verdict(state):
    env = dict(os.environ, VERIFY_STATE=str(state),
               PATH=str(here / "fake") + os.pathsep + os.environ.get("PATH", ""))
    try:
        r = subprocess.run([sys.executable, str(script)], cwd=project, env=env, text=True,
                           capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", f"no result after {TIMEOUT} s (a retry loop? locally the endpoint is always in sync)"
    lines = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    if r.returncode == 0 and last == "PASS":
        return "PASS", last
    if r.returncode == 1 and last == "FAIL":
        return "FAIL", next((l for l in lines if l.startswith("FAIL") and l != "FAIL"), last)
    err = r.stderr.strip().splitlines()
    return "CRASH", f"exit {r.returncode}, last line {last!r}" + (f", stderr: {err[-1]}" if err else "")


if not script.is_file():
    say(False, "checks/check_orders.py exists", f"{script} not found")
else:
    with tempfile.TemporaryDirectory(prefix="210-04-") as tmp:
        tmp = pathlib.Path(tmp)
        names = {"empty": "state-b", "canceled": "state-c", "done": "state-a"}
        for name, neutral in names.items():
            shutil.copytree(here / "states" / name, tmp / neutral)
        changed = tmp / "state-d"
        shutil.copytree(here / "states" / "done", changed)
        con = sqlite3.connect(changed / "endpoint.db")
        con.execute("UPDATE orders SET amount = amount + 1.00 WHERE order_id = 1")
        con.commit()
        con.close()
        got = []
        for name, want in (("empty", "FAIL"), ("canceled", "FAIL"), ("done", "PASS")):
            result, detail = verdict(tmp / names[name])
            got.append(result)
            hint = {"empty": "the job says Completed, but was the table ever written?",
                    "canceled": "the rows look right, but which run wrote them? Compare commit time and run start",
                    "done": detail}[name] if result == "PASS" else detail
            say(result == want, f"{name}: {result}, expected {want}", hint)
        say(got.count("PASS") == 1, f"exactly one PASS ({', '.join(got)})")
        result, detail = verdict(changed)
        say(result == "FAIL", f"done, one order changed in orders: {result}, expected FAIL",
            "compute the expected values from orders, not from orders_by_region or from numbers in the script"
            if result == "PASS" else detail)
print("PASS" if ok else "NOT YET")
sys.exit(0 if ok else 1)
