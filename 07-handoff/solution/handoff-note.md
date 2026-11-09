# Handoff note

2026-11-05, session sales-migration (updates the note of 2026-11-04)

## State

- Fabric pipeline `workspace/pl_sales_nightly.DataPipeline/` is rebuilt from `adf/pl_sales_nightly.json` (Lookup → ForEach → one Copy per table) (migration.md:5).
- Dev test run on 2026-11-04 01:00 UTC: 26 of 30 copies succeeded (logs/testrun-2026-11-04.log:32).
- Failed in the first seconds: dbo.Invoices, dbo.Payments, dbo.Returns, dbo.Shipments (logs/testrun-2026-11-04.log:2-5).
- All four: "Logon failed for login 'svc_fabric_ingest' due to trigger execution." (logs/testrun-2026-11-04.log:2-5). The source logon trigger rejects a logon above the pipeline's share (config/source.yaml:7-11).
- Gateway ruled out: heartbeat ok, 2 of 2 members online, no errors in the run window (logs/gateway-2026-11-04.log:1-9).
- Limit: at most 16 copies in parallel. The logon trigger gives each of the 3 pipelines on the login an equal share of 48 sessions, one session per copy (config/source.yaml:7-12).
- The source has a maintenance window on Sundays 01:00-03:00 (config/source.yaml:14). A run at 01:00 falls into it on Sundays. The 2026-11-04 test run was on a Wednesday, so it was not affected.

## Findings (2026-11-05)

- Cause: the Fabric ForEach had `"isSequential": false` and no `batchCount` (pipeline-content.json before this session's fix). The ADF pipeline has `"batchCount": 8` (adf/pl_sales_nightly.json:20); it was dropped in the rebuild.
- With no batchCount, a ForEach runs up to 20 iterations in parallel (Microsoft ForEach documentation, not in a repo file). 20 > 16.
- The test run log matches 20 parallel starts: 4 rejected at 01:00:04 (logs/testrun-2026-11-04.log:2-5) and 16 that succeeded between 01:01:53 and 01:02:58 (logs/testrun-2026-11-04.log:6-21). The remaining 10 started as slots freed up, e.g. dbo.InvoiceLines ended 01:04:23 after 150s, so it started 01:01:53 when dbo.Customers ended (logs/testrun-2026-11-04.log:6,22).
- Fix applied: `"batchCount": 8` added to the ForEach (workspace/pl_sales_nightly.DataPipeline/pipeline-content.json:19), same as ADF.

## Open question

Does the fixed pipeline run all 30 copies without trigger rejections? Not tested yet.

## Next step

Run the pipeline again in the dev workspace and check that 30 of 30 copies succeed. Before production, pick a schedule that avoids the Sunday 01:00-03:00 maintenance window (config/source.yaml:14).

## Files

migration.md, workspace/pl_sales_nightly.DataPipeline/pipeline-content.json, config/source.yaml, logs/testrun-2026-11-04.log, logs/gateway-2026-11-04.log, adf/pl_sales_nightly.json (read-only)
