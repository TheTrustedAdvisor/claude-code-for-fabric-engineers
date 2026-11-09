# Exercise 210-04-verify

Companion exercise to part 4 of the series "Learning Claude for Microsoft Fabric": "Fabric job Completed: did Claude Code really update the table?". Runs locally; only the optional step uses your own Fabric workspace.

> **Status:** Ready: `python3 check.py <your project>` fails before you start and passes on `solution/`.

## Task

Write a check with Claude that decides from the sources whether the table `orders_by_region` is really up to date after the last run of the notebook `nb_kurs`: the job status, the table's Delta log, and the rows through the SQL endpoint. It runs locally, with a fake `fab` command, a folder that stands in for the Delta log, and a small SQLite database as the endpoint, so you need no capacity.

There are three states, and the right answer for each is known:

| State | What happened | Right answer |
|---|---|---|
| `states/empty` | The notebook ran and reports Completed, but `orders_by_region` was never written: no Delta log, no table on the endpoint. | FAIL |
| `states/canceled` | A good run wrote the table. A later run was canceled 25 seconds in and still reports Completed, with no failure reason. It wrote nothing; the endpoint shows the earlier run's rows, which look right. Only the commit time gives it away. | FAIL |
| `states/done` | A run after that rebuilt the table: Completed, a commit after the run started, rows equal a GROUP BY over `orders`. | PASS |

The data is the course seed: 1,000 orders in four regions (North, East, South, West). `states/build.py` creates the states; you don't need to run it.

## What a good result looks like

FAIL, FAIL, PASS: exactly one PASS. Your `checks/check_orders.py` passes only if all three hold:

1. The last run of `nb_kurs` has status Completed.
2. `orders_by_region` has a Delta commit after that run started (allow 60 seconds of clock difference).
3. Through the SQL endpoint, orders and amount per region in `orders_by_region` equal a GROUP BY over `orders` (amounts within 0.01), and the total is 1,000 orders.

The expected values come from the input, never from the output: `check.py` also runs your script on a copy of `done` in which one order costs 1.00 more, and expects FAIL there. The script prints one line per check, then PASS or FAIL, and exits 1 on FAIL. A reference is in `solution/checks/check_orders.py`; look at it after your own attempt.

## Optional

Use your own workspace with the same seed: four regions, a thousand orders.

1. `python3 states/build.py --csv orders.csv` writes the 1,000 orders. Upload the file to a lakehouse and load it as the table `orders`.
2. Create a notebook that writes `orders_by_region`, for example:
   ```python
   df = spark.read.table("orders")
   out = df.groupBy("region").agg({"amount": "sum", "order_id": "count"})
   out = out.withColumnRenamed("sum(amount)", "amount").withColumnRenamed("count(order_id)", "orders")
   out.write.mode("overwrite").format("delta").saveAsTable("orders_by_region")
   ```
3. Run it with `fab job run <workspace>.Workspace/<notebook>.Notebook`, then let your check read the real sources: `fab job run-list` for the runs, `fab ls -l <workspace>.Workspace/<lakehouse>.Lakehouse/Tables/orders_by_region/_delta_log` for the commit times (in a lakehouse with schemas, `Tables/dbo/orders_by_region`), and any SQL client on the lakehouse's SQL analytics endpoint for the rows. The endpoint syncs in the background, so retry (3) for up to 5 minutes when (2) passes and (3) doesn't. Locally you don't need that retry: the database is always in sync.
4. To see the `canceled` state for real: `fab job start …`, wait about 25 seconds, `fab job run-cancel … --id <job id> --wait`, then read the run's status and the Delta log. Whether the run reports Completed or Cancelled, and whether it committed, depends on how far it got; only the commit time tells you.

## How to run it

You need Claude Code, Bash and Python 3 as `python3` (standard library only). On Windows, use Git Bash for the commands here; `fake/fab.cmd` lets a Python check find the fake through `shutil.which("fab")`.

1. In a terminal, from this folder (`210-04-verify/` in the companion repo):
   ```
   ./setup.sh canceled /var/tmp/210-04
   ```
   `setup.sh <state> [folder]` creates the project in the folder on first use (default `/var/tmp/210-04`, outside any Git repository and without a `CLAUDE.md` above it), copies the fake `fab` to `lab/fake/` and the chosen state to `lab/current/`, and writes `env.sh`. Run it again with another state to switch; your `CLAUDE.md` and `checks/` stay as they are.
2. `cd /var/tmp/210-04 && source env.sh`. That puts the fake `fab` on the PATH and sets `VERIFY_STATE` to `lab/current`, where the fake and your check read the state. Try `fab job run-list tta210-lab.Workspace/nb_kurs.Notebook`.
3. Start `claude` from the same shell, so it inherits PATH and `VERIFY_STATE`. The project's `CLAUDE.md` names the fake `fab`, the Delta log folder and the database, and how to read them. `.claude/settings.json` allows the read-only `fab` calls and `python3 checks/check_orders.py`; on the first start choose "Yes, I trust this folder".
4. Ask for the check. The prompt from the video works nearly verbatim; locally, drop the retry sentence:

   > Write checks/check_orders.py. It passes only if all of these hold: (1) the last run of nb_kurs has status Completed, (2) orders_by_region has a Delta commit after that run started, (3) through the SQL endpoint, orders and amount per region in orders_by_region equal a GROUP BY over orders, and the total is 1000 orders. Treat amounts as equal within 0.01, and allow 60 seconds of clock difference on (2). Print one line per check, then PASS or FAIL, exit 1 on FAIL. Don't run the notebook. Run the check once and show me the output.

   With the state `canceled`, the right output ends in FAIL, although (1) and (3) pass.
5. Switch states in a second terminal (`./setup.sh empty /var/tmp/210-04`, then `done`) and run `python3 checks/check_orders.py` there after `source env.sh`, or ask Claude to run it again. No restart needed: `VERIFY_STATE` keeps pointing at `lab/current`.
6. Grade it: `python3 check.py /var/tmp/210-04`. It runs your script against all three states (and the changed copy of `done`) and prints PASS when you get FAIL, FAIL, PASS.
