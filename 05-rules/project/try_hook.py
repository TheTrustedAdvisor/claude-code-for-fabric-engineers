"""Feed one shell command to the project's PreToolUse hook and print what it decides.

    python3 try_hook.py 'bash deploy.sh prod'
"""
import json
import os
import pathlib
import subprocess
import sys

if len(sys.argv) != 2:
    sys.exit("usage: python3 try_hook.py '<command>'")

project = pathlib.Path(__file__).resolve().parent
hook = project / ".claude" / "hooks" / "block-prod.py"
if not hook.is_file():
    sys.exit(f"no hook in this project: {hook}")

event = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
         "tool_input": {"command": sys.argv[1]}, "cwd": str(project)}
env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
run = subprocess.run([sys.executable, str(hook)], input=json.dumps(event), capture_output=True,
                     text=True, cwd=project, env=env)
if run.returncode not in (0, 2):
    print(f"hook failed (exit {run.returncode}); with onFailure \"block\" Claude Code would block this call")
    print(run.stderr.strip())
    sys.exit(1)
decision = None
if run.returncode == 2:
    decision = "deny"
elif run.stdout.strip():
    try:
        decision = json.loads(run.stdout).get("hookSpecificOutput", {}).get("permissionDecision")
    except (ValueError, AttributeError):
        print("hook failed: its output is not valid JSON")
        sys.exit(1)
print("blocked" if decision == "deny" else "passes")
