# Lab: did the notebook really update the table? (local)

This folder stands in for a Fabric workspace. Nothing here talks to Fabric; there is no capacity and no sign-in.

- Workspace `tta210-lab`, lakehouse `lh_kurs`, notebook `nb_kurs`. The notebook reads the table `orders` (1,000 rows: `order_id`, `region`, `amount`, `order_date`) and writes `orders_by_region` (`region`, `orders`, `amount`) with CREATE OR REPLACE TABLE AS SELECT.
- `fab` on the PATH is a read-only fake of the Fabric CLI (`lab/fake/fab`). It knows three calls:
  - `fab job run-list tta210-lab.Workspace/nb_kurs.Notebook`: the runs as a table (`id`, `status`, `startTimeUtc`, `endTimeUtc`, `failureReason`). Times are UTC without a zone, with seven decimal digits.
  - `fab job run-status tta210-lab.Workspace/nb_kurs.Notebook --id <job id>`: one run, one `key: value` per line.
  - `fab ls -l tta210-lab.Workspace/lh_kurs.Lakehouse/Tables/orders_by_region/_delta_log`: the Delta commit files with their time (`lastModified`, GMT, whole seconds). If the table was never written, this fails with `[NotFound]`.
- The Delta log is the folder `$VERIFY_STATE/onelake/Tables/orders_by_region/_delta_log/`. Each commit file holds a `commitInfo` line with `timestamp` (milliseconds since 1970, UTC) and `operation`.
- The SQL analytics endpoint is the SQLite database `$VERIFY_STATE/endpoint.db` with the tables `orders` and `orders_by_region`. Open it read-only (`sqlite3.connect(f"file:{path}?mode=ro", uri=True)`, standard library). Here it is always in sync; in Fabric it syncs in the background.
- `VERIFY_STATE` and the PATH come from `env.sh` (`source env.sh` before starting Claude Code). The current state (`empty`, `canceled` or `done`) is switched with `setup.sh` from the companion repo, by the person, not by you.
- Never run, start or cancel the notebook. The fake refuses anyway.
- Checks go in `checks/`, Python 3 standard library only. Don't hard-code expected values: compute them from `orders`.
