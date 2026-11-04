"""PreToolUse hook for Bash: deny a deploy to prod."""
import json
import re
import sys

DEPLOY = re.compile(r"deploy\.(sh|py)\b")
PROD = re.compile(r"""(?:^|[\s='"])(prod|production)(?=$|[\s'"/;)])""", re.I)
SPLIT = re.compile(r"&&|\|\||[;|&\n]")

event = json.load(sys.stdin)
command = event.get("tool_input", {}).get("command", "")
if any(DEPLOY.search(part) and PROD.search(part) for part in SPLIT.split(command)):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Blocked by hook: deploy to production.",
    }}))
sys.exit(0)
