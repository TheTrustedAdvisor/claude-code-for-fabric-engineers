# Exercise 210-07-tmdl

Companion exercise to part 7 of the series "Learning Claude for Microsoft Fabric": "Fabric semantic models in TMDL: can you trust Claude Code's edits?". Runs locally; only the optional step uses your own Fabric workspace.

> **Status:** Ready: `python3 check.py` fails on `project/` as you get it and passes once `project/` holds the model from `solution/`.

## Task

`project/sm_kurs.SemanticModel/` is a semantic model as a Power BI project in TMDL, the way `fab export` writes it: one table `orders` (Direct Lake on a lakehouse table with the same name), four columns, no measures. `project/CLAUDE.md` holds the modeling conventions.

Work with Claude, without Power BI:

1. Add a measure `Total Revenue` to the table `orders`: the sum of `amount`, formatted by the conventions.
2. Rename the column `amount` to `Sales Amount` in the model only, and update every measure that uses it. The lakehouse table keeps its column name.

## What a good result looks like

```
[OK] the diff touches only definition/tables/orders.tmdl
[OK] column 'Sales Amount' reads sourceColumn amount
[OK] measure 'Total Revenue' = SUM(orders[Sales Amount]), formatString #,0.00
East    54901.63 = 54901.63
North   68531.33 = 68531.33
South   66766.59 = 66766.59
West    61999.88 = 61999.88
PASS
```

`check.py` does what the video does with two checks. The diff: it compares every model file with `base/` (the model as exported; leave that folder alone), and only `orders.tmdl` may differ. The number: a small evaluator computes your measure per region over `seed/orders.csv` (the same 1,000 rows as the lab in the video, seed 210) and compares it with totals that come from the seed, not from the model. It only knows `SUM(orders[<column>])`, which is all the task needs. A reference is in `solution/`; look at it after your own attempt.

## How to run it

You need Claude Code and Python 3 as `python3` (standard library only). No capacity, no sign-in.

1. From `project/` in this folder (`210-07-tmdl/project/` in the companion repo), start `claude`.
2. Ask, for example:

   > Add a measure Total Revenue to the table orders: the sum of amount, formatted like the conventions in CLAUDE.md. Edit only the TMDL. Show me the diff.

   Then:

   > Rename the column amount to Sales Amount in the model only, and update every measure that uses it. Show me the diff.

3. Read each diff before you go on. Then grade it from `210-07-tmdl/`: `python3 check.py`. To start over: `git checkout -- project/`.

## Optional: your own workspace

You need a workspace on a Fabric capacity you can write to (Contributor is enough), a lakehouse `lh_kurs` with a table `orders` (load `seed/orders.csv`), and the Fabric CLI (`python -m pip install ms-fabric-cli`, then `fab auth login`). A semantic model is a Power BI item: to create one in a shared workspace you need a Power BI Pro or Premium Per User license (or an individual trial), and on capacities below F64 viewing Power BI content needs one too.

1. Put your workspace ID and lakehouse ID into `project/sm_kurs.SemanticModel/definition/expressions.tmdl` (the two placeholders in the OneLake URL).
2. Publish: `fab import <your workspace>.Workspace/sm_kurs.SemanticModel -i project/sm_kurs.SemanticModel -f`.
3. Compare the measure with the source: a DAX query against the model (for example through the Execute Queries REST API, `EVALUATE SUMMARIZECOLUMNS('orders'[region], "r", [Total Revenue])`) and `SELECT region, SUM(amount) FROM dbo.orders GROUP BY region` on the lakehouse's SQL analytics endpoint. The two must match per region.

A successful publish only says the definition was accepted. The comparison with the source tells you the measure is right.
