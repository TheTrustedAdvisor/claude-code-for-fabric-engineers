# Orders lakehouse

A Fabric project in Git: notebooks that load order data into a lakehouse.

- Lakehouse tables use snake_case with a layer prefix: bronze_, silver_ or gold_.
- Every notebook starts with a markdown cell that names its source and target tables.
- Deploy only to the dev workspace. Never deploy to the production workspace.
