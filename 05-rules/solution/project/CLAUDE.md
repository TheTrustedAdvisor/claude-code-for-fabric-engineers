# Notebook project

A Fabric notebook project in Git, deployed with `deploy.sh` or `deploy.py` to a dev or a prod workspace.

- Deploy only to dev, with `./deploy.sh dev`. Never deploy to the production workspace.
- Every notebook starts with a markdown cell that names its source and target tables.
- Before a deploy, show the command you're about to run.
