# Exercise 210-04-verify

Companion exercise to part 4 of the series "Learning Claude for Microsoft Fabric": "Fabric job Completed: did Claude Code really update the table?". Runs locally; only the optional step uses your own Fabric workspaces.

> **Status:** In preparation. The full exercise (setup, project, check.py, solution) is published together with the video.

## Task

Write a check with Claude that decides from the sources (job status, Delta log, SQL endpoint) whether a table is really up to date. Runs locally against a fake fab, a folder for the Delta log and a small database for the endpoint, in three states: empty, cancelled, done.

## What a good result looks like

FAIL, FAIL, PASS: exactly one PASS.

## Optional

Your own workspace: 4 regions, 1,000 orders.
