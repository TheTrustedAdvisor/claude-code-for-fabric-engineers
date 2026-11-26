# orders-team

Fabric project for the orders pipeline: lakehouse lh_kurs, notebook nb_kurs, table orders_by_region.

Environments:
- dev: each person's own workspace, read from FABRIC_DEV_WORKSPACE
  (set it in your .claude/settings.local.json, never here)
- prod: orders-prod, protected by the hook in .claude/hooks/block_protected.py

Rules:
- Before any write, run `fab auth status`.
- Run the notebook: `fab job run <dev workspace>.Workspace/nb_kurs.Notebook`
- After a job or a deployment, use the fabric-verify skill.
