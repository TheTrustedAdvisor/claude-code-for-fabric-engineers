# Handoff note

2026-11-04, session sales-migration

## State

- Fabric pipeline `workspace/pl_sales_nightly.DataPipeline/` is rebuilt from `adf/pl_sales_nightly.json` (Lookup → ForEach → one Copy per table) (migration.md:5).
- Dev test run on 2026-11-04 01:00 UTC: 26 of 30 copies succeeded (migration.md:6, citing logs/testrun-2026-11-04.log:32).
- Failed in the first seconds: dbo.Invoices, dbo.Payments, dbo.Returns, dbo.Shipments (migration.md:10, citing logs/testrun-2026-11-04.log:2-5).
- All four: "Logon failed for login 'svc_fabric_ingest' due to trigger execution." (migration.md:11). No log line is cited for this, and neither is the claim that the source DB (not Fabric) rejects the logons.
- Gateway ruled out: no errors or restarts in the run window (migration.md:12, citing logs/gateway-2026-11-04.log:1-9).
- Limit, read in config/source.yaml in session sales-migration: at most 16 copies in parallel. The logon trigger gives each of the 3 pipelines on the login an equal share of 48 sessions, one session per copy (config/source.yaml:7-12).
- The source has a maintenance window on Sundays 01:00-03:00 (config/source.yaml:14). A run at 01:00 falls into it on Sundays.

## Open question

Does the ForEach run more than 16 copies at once?

## Next step

Check the ForEach batch count in `workspace/pl_sales_nightly.DataPipeline/pipeline-content.json` against the limit of 16. Not read yet.

## Files

migration.md, workspace/pl_sales_nightly.DataPipeline/pipeline-content.json, config/source.yaml, logs/testrun-2026-11-04.log, logs/gateway-2026-11-04.log, adf/pl_sales_nightly.json (read-only)
