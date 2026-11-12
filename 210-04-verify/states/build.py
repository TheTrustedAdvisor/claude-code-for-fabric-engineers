"""Build the three states of exercise 210-04 (empty, canceled, done) from the course seed.

    python3 states/build.py                 # rewrite states/empty, states/canceled, states/done
    python3 states/build.py --csv FILE      # write the 1,000 orders as CSV, for the optional step in your own workspace

Each state folder holds what a check can see after a run of nb_kurs:
  jobs.json                                              runs of nb_kurs, read by the fake fab (job run-list, run-status)
  onelake/Tables/orders_by_region/_delta_log/*.json      Delta commits, listed by the fake fab (ls -l)
  endpoint.db                                            SQLite stand-in for the SQL analytics endpoint

Standard library only. Same seed as the course lab: SEED 210, 1,000 orders, four regions.
"""
import csv
import datetime
import json
import pathlib
import random
import shutil
import sqlite3
import sys

ROWS, SEED = 1000, 210
REGIONS = ["North", "East", "South", "West"]
FIRST_DAY, DAYS = datetime.date(2026, 1, 1), 90
WORKSPACE, NOTEBOOK, LAKEHOUSE = "tta210-lab", "nb_kurs", "lh_kurs"
NOTEBOOK_ID = "6f1c2a8e-3b7d-4e52-9a41-0c5d8e7f2b19"
TABLE_ID = "b2e47d90-5c1a-4f3e-8d26-7a9b0e1c4f53"
HERE = pathlib.Path(__file__).resolve().parent


def orders():
    """Same generator as the course lab: same seed, same rows on every machine."""
    rnd = random.Random(SEED)
    ids = list(range(1, ROWS + 1))
    region = [REGIONS[rnd.randrange(4)] for _ in ids]
    amount = [round(rnd.uniform(10, 500), 2) for _ in ids]
    day = [(FIRST_DAY + datetime.timedelta(days=rnd.randrange(DAYS))).isoformat() for _ in ids]
    return list(zip(ids, region, amount, day))


def by_region(rows):
    out = {}
    for _, region, amount, _ in rows:
        n, total = out.get(region, (0, 0.0))
        out[region] = (n + 1, total + amount)
    return sorted((r, n, total) for r, (n, total) in out.items())


def run(job_id, start, end, status="Completed"):
    return {"id": job_id, "itemId": NOTEBOOK_ID, "jobType": "RunNotebook", "invokeType": "Manual",
            "status": status, "startTimeUtc": start, "endTimeUtc": end, "failureReason": None}


def epoch_ms(utc):
    return int(datetime.datetime.fromisoformat(utc).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)


def commit(version, utc):
    """One Delta commit file: newline-delimited actions, as Spark writes them (shortened)."""
    actions = [{"commitInfo": {
        "timestamp": epoch_ms(utc), "operation": "CREATE OR REPLACE TABLE AS SELECT",
        "operationParameters": {"isManaged": "true", "partitionBy": "[]"},
        "notebook": {"notebookId": NOTEBOOK_ID},
        "isolationLevel": "Serializable", "isBlindAppend": False,
        "operationMetrics": {"numFiles": "1", "numOutputRows": "4"}}}]
    if version == 0:
        actions.append({"protocol": {"minReaderVersion": 1, "minWriterVersion": 2}})
        actions.append({"metaData": {"id": TABLE_ID, "format": {"provider": "parquet", "options": {}},
                                     "schemaString": json.dumps({"type": "struct", "fields": [
                                         {"name": "region", "type": "string", "nullable": True, "metadata": {}},
                                         {"name": "amount", "type": "double", "nullable": True, "metadata": {}},
                                         {"name": "orders", "type": "long", "nullable": False, "metadata": {}}]}),
                                     "partitionColumns": [], "configuration": {}, "createdTime": epoch_ms(utc)}})
    else:
        actions.append({"remove": {"path": f"part-0000{version - 1}-snappy.parquet",
                                   "deletionTimestamp": epoch_ms(utc), "dataChange": True}})
    actions.append({"add": {"path": f"part-0000{version}-snappy.parquet", "partitionValues": {},
                            "size": 1310, "modificationTime": epoch_ms(utc), "dataChange": True}})
    return "\n".join(json.dumps(a, separators=(",", ":")) for a in actions) + "\n"


# Runs of nb_kurs, UTC as the Fabric job scheduler reports it (seven decimal digits, no zone).
EARLY = run("0b6d6c1e-7f2a-4a8e-9c35-2d1f4e8a6b70", "2026-11-09T13:02:31.5520114", "2026-11-09T13:03:14.0072215")
GOOD = run("4a2f9d13-8c6e-4b71-a0d5-9e3b7c1f2a48", "2026-11-09T13:10:12.4410273", "2026-11-09T13:10:55.1302311")
CANCELED = run("c7e5b2a9-1d4f-4e83-b6a0-58f2d9c3e714", "2026-11-09T13:17:40.6980625", "2026-11-09T13:18:10.9713135")
RERUN = run("e91a4c6d-2b8f-4d07-8e53-a6c1f0b9d327", "2026-11-09T13:24:05.2216471", "2026-11-09T13:24:47.9015530")
# Commit times inside the run that wrote them; the canceled run wrote nothing.
COMMIT_GOOD = "2026-11-09T13:10:49.812"
COMMIT_RERUN = "2026-11-09T13:24:42.337"

STATES = {
    # The notebook ran and said Completed, but orders_by_region was never written.
    "empty": {"runs": [EARLY], "commits": []},
    # A good run wrote the table; a later run was canceled 25 s in, reports Completed with no failure reason,
    # and wrote nothing. The endpoint still shows the good run's rows, which look right.
    "canceled": {"runs": [GOOD, CANCELED], "commits": [COMMIT_GOOD]},
    # The table was rebuilt by a run after that: Completed, and a commit after the run started.
    "done": {"runs": [GOOD, CANCELED, RERUN], "commits": [COMMIT_GOOD, COMMIT_RERUN]},
}


def build(name, spec, rows):
    folder = HERE / name
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir()
    (folder / "jobs.json").write_text(json.dumps(
        {"workspace": WORKSPACE, "lakehouse": LAKEHOUSE, "item": NOTEBOOK, "itemType": "Notebook",
         "runs": spec["runs"]}, indent=2) + "\n")
    if spec["commits"]:
        log = folder / "onelake" / "Tables" / "orders_by_region" / "_delta_log"
        log.mkdir(parents=True)
        for version, utc in enumerate(spec["commits"]):
            (log / f"{version:020d}.json").write_text(commit(version, utc))
    db = sqlite3.connect(folder / "endpoint.db")
    db.execute("CREATE TABLE orders (order_id INTEGER NOT NULL, region TEXT NOT NULL, amount REAL NOT NULL, "
               "order_date TEXT NOT NULL)")
    db.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", rows)
    if spec["commits"]:
        db.execute("CREATE TABLE orders_by_region (region TEXT, amount REAL, orders INTEGER)")
        db.executemany("INSERT INTO orders_by_region VALUES (?, ?, ?)",
                       [(r, total, n) for r, n, total in by_region(rows)])
    db.commit()
    db.execute("VACUUM")
    db.close()


def main():
    rows = orders()
    if sys.argv[1:2] == ["--csv"] and len(sys.argv) == 3:
        with open(sys.argv[2], "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["order_id", "region", "amount", "order_date"])
            w.writerows((i, r, f"{a:.2f}", d) for i, r, a, d in rows)
        print(f"wrote {len(rows)} orders to {sys.argv[2]}")
        return
    if sys.argv[1:]:
        sys.exit(__doc__)
    for name, spec in STATES.items():
        build(name, spec, rows)
    for region, n, total in by_region(rows):
        print(f"{region:<6} {n:>4} {total:>10.2f}")
    print(f"total  {len(rows):>4} {sum(a for _, _, a, _ in rows):>10.2f}")


if __name__ == "__main__":
    main()
