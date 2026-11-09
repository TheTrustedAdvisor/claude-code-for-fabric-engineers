# Exercise 210-07-tmdl

Companion exercise to part 7 of the series "Learning Claude for Microsoft Fabric": "Fabric semantic models in TMDL: can you trust Claude Code's edits?". Runs locally; only the optional step uses your own Fabric workspaces.

> **Status:** In preparation. The full exercise (setup, project, check.py, solution) is published together with the video.

## Task

A semantic model as a TMDL project folder. Add a measure and rename a column with Claude, without Power BI.

## What a good result looks like

The diff touches only the expected file; a small evaluation of the measure over the seed data gives the expected sums for all 4 regions.

## Optional

Run the measure as real DAX against your own model.
