"""Check your hook for exercise 210-03.

    python3 check.py <project folder>

Feeds the four sample events to <project>/.claude/hooks/block_protected.py and expects exit codes 2, 2, 2, 0.
Then checks the registration in <project>/.claude/settings.json: PreToolUse, a matcher that covers Bash and
mcp__ tools, and onFailure "block". Event 5 is printed for you to think about; it is not graded.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

here = pathlib.Path(__file__).resolve().parent
project = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "project").resolve()
hook = project / ".claude" / "hooks" / "block_protected.py"
ok = True


def say(good, label, why=""):
    global ok
    ok &= good
    print(f"{'ok  ' if good else 'FAIL'}  {label}" + ("" if good or not why else f": {why}"))


def run(event):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    r = subprocess.run([sys.executable, str(hook)], input=event.read_text(), text=True, capture_output=True, env=env)
    return r.returncode, r.stderr.strip()


if not hook.is_file():
    say(False, "hook exists", f"{hook} not found")
else:
    want = {"1": 2, "2": 2, "3": 2, "4": 0}
    for n, code in want.items():
        got, err = run(here / "events" / f"{n}.json")
        say(got == code, f"event {n}: exit {got}, expected {code}", err or "no reason on stderr")
        if code == 2 and got == 2:
            say(bool(err), f"event {n}: reason on stderr", "print which workspace matched")
    got, _ = run(here / "events" / "5.json")
    print(f"note  event 5 (python3 scripts/run_from_config.py): exit {got}. Why can't the hook see this one?")
try:
    settings = json.loads((project / ".claude" / "settings.json").read_text())
    entries = settings.get("hooks", {}).get("PreToolUse", [])
    good = [e for e in entries if all(re.search(e.get("matcher", ""), t) for t in ("Bash", "mcp__fabric-core__list_items"))
            and any("block_protected.py" in h.get("command", "") and h.get("onFailure") == "block" for h in e.get("hooks", []))]
    say(bool(good), "registered under PreToolUse for Bash and MCP, onFailure block",
        "matcher must match Bash and mcp__…, the hook entry needs \"onFailure\": \"block\"")
except (OSError, ValueError) as e:
    say(False, "settings.json readable", str(e))
print("PASS" if ok else "NOT YET")
sys.exit(0 if ok else 1)
