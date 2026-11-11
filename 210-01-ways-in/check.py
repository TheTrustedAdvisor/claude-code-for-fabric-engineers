"""Check your choices for exercise 210-01-ways-in.

    python3 check.py <project folder>

Reads <project>/ways.yaml (one way per task) and <project>/.claude/settings.json (the allow list) and prints one
line per task, then PASS or FAIL (exit 1 on FAIL). It needs nothing but Python 3: no Fabric, no Claude Code.

A task passes when its way is one that can do the job (see tasks.md) and exactly one allow rule covers it, written
for that way. The allow list passes when every rule covers one of the five tasks and nothing broader: no rule for a
whole tool or server (`Bash`, `Bash(fab *)`, `Bash(fab api *)`, `mcp__fabric-core`, `mcp__fabric-core__*`).
"""
import json
import pathlib
import re
import sys

project = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "project").resolve()
WS, NB = "tta210-lab.Workspace", "nb_kurs.Notebook"

# per task: accepted ways, each with the allow rules that cover the task on that way (regular expressions)
ANSWERS = {
    "task-1": {"fab": [rf"Bash\(fab job run ({re.escape(WS)}/{re.escape(NB)}|{re.escape(WS)}/\*|\*)( \*)?\)"],
               "why": "only fab can run it: the Core MCP server has no tool that runs a job"},
    "task-2": {"fab": [rf"Bash\(fab job run-list ({re.escape(WS)}/{re.escape(NB)}|{re.escape(WS)}/\*|\*)( \*)?\)"],
               "why": "unattended means no browser: fab signs in as a service principal, Core MCP needs a browser sign-in"},
    "task-3": {"core mcp": [r"mcp__fabric-core__search_catalog"],
               "why": "an overview across workspaces is what search_catalog on the Core MCP server is for"},
    "task-4": {"core mcp": [r"mcp__fabric-core__add_workspace_role"],
               "fab": [r"Bash\(fab acl set (tta210-lab\.Workspace|\*)( \*)?\)"],
               "why": "granting must be allowed, removing must not: add_workspace_role, or fab acl set (never fab acl rm)"},
    "task-5": {"fab api": [r"Bash\(fab api (?=[^)]*refreshMetadata)(?=[^)]*(-X|--method) (post|POST))[^)]*\)"],
               "why": "fab has no command for it: fab api workspaces/<id>/sqlEndpoints/<id>/refreshMetadata -X post"},
}
TOO_BROAD = re.compile(r"^(Bash|Bash\(\*\)|Bash\(fab( \*|:\*)?\)|Bash\(fab (api|job|acl)( \*|:\*)\)|"
                       r"mcp__fabric-core(__\*)?|mcp__\*)$")
WAYS = {"fab", "fab api", "core mcp"}
ok = True


def say(good, label, why=""):
    global ok
    ok &= good
    print(f"{'ok  ' if good else 'FAIL'}  {label}" + ("" if good or not why else f": {why}"))


def ways(path):
    out = {}
    for line in path.read_text().splitlines():
        m = re.match(r"\s*(task-[1-5])\s*:\s*([^#]*)", line)
        if m:
            out[m.group(1)] = m.group(2).strip().lower()
    return out


try:
    chosen = ways(project / "ways.yaml")
    allow = json.loads((project / ".claude" / "settings.json").read_text()).get("permissions", {}).get("allow", [])
except (OSError, ValueError) as e:
    print(f"FAIL  cannot read the project: {e}")
    print("FAIL")
    sys.exit(1)

used = set()
for task, answer in ANSWERS.items():
    way = chosen.get(task, "")
    if way not in WAYS:
        say(False, task, f"pick one of fab, fab api, core mcp (got {way!r})")
        continue
    if way not in answer:
        say(False, f"{task} ({way})", answer["why"])
        continue
    hits = [r for r in allow if any(re.fullmatch(p, r) for p in answer[way])]
    used.update(hits)
    if len(hits) == 1:
        say(True, f"{task} ({way}): {hits[0]}")
    elif not hits:
        say(False, f"{task} ({way})", "no allow rule covers it on this way")
    else:
        say(False, f"{task} ({way})", f"{len(hits)} rules cover it, keep one: {hits}")

broad = [r for r in allow if TOO_BROAD.match(r)]
extra = [r for r in allow if r not in used and r not in broad]
say(not broad, "allow list: nothing broader than a task", f"too broad: {broad}")
say(not extra, "allow list: nothing besides the five tasks", f"not needed: {extra}")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
