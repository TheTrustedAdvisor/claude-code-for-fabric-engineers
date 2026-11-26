---
name: fabric-verify
description: Run after any Fabric job or deployment to decide whether the result is real.
---
Run `python3 checks/check_orders.py`. Quote its lines. Say done only if it prints PASS.
If it prints FAIL, show the output and stop. Never derive expected values from the output.
