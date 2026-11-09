# Migration of pl_sales_nightly: state on 2026-11-04, afternoon

## Done

- The Fabric pipeline is in `workspace/pl_sales_nightly.DataPipeline/`, rebuilt from `adf/pl_sales_nightly.json`: a Lookup that lists the tables, a ForEach over them, one Copy activity per table.
- Test run in the dev workspace, last night at 01:00: 26 of 30 table copies succeeded (`logs/testrun-2026-11-04.log:32`).

## What failed

- 4 copies failed in the first seconds of the run: dbo.Invoices, dbo.Payments, dbo.Returns, dbo.Shipments (`logs/testrun-2026-11-04.log:2-5`).
- All four with the same source error: "Logon failed for login 'svc_fabric_ingest' due to trigger execution." The rejection comes from the source database, not from Fabric.
- The gateway is ruled out: its log shows no errors and no restarts in the run window (`logs/gateway-2026-11-04.log:1-9`).

## Open question

Why does the source reject these logons, and how many copies may the ForEach run at the same time?

## Not read yet

- `config/source.yaml` (connection and limits of the source, from the DBA team)
- the ForEach settings in `workspace/pl_sales_nightly.DataPipeline/pipeline-content.json`
