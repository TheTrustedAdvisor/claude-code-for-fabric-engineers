# Sales pipeline migration

We're moving the nightly pipeline pl_sales_nightly from Azure Data Factory (adf/) to a Fabric pipeline (workspace/).

- Every fact you state cites its source as file:line.
- adf/ is the old pipeline. Read it, never edit it.
- All times are UTC.
