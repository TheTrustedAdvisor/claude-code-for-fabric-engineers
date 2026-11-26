#!/usr/bin/env python3
"""PreToolUse hook: stop any call whose input names a protected Fabric workspace (name or id).

Reads the event as JSON on stdin. Exit 2 with the reason on stderr blocks the call; exit 0 lets it through.
It sees text only: a script that reads the workspace from a file passes (event 5).
"""
import json
import os
import sys

event = json.load(sys.stdin)
here = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
with open(os.path.join(here, ".claude", "protected-workspaces.json"), encoding="utf-8") as f:
    protected = json.load(f)["protected"]
text = json.dumps(event.get("tool_input", {})).lower()
for ws in protected:
    for key in ("name", "id"):
        if ws[key].lower() in text:
            print(f"Blocked: protected workspace {ws['name']} ({key} found in the call)", file=sys.stderr)
            sys.exit(2)
sys.exit(0)
