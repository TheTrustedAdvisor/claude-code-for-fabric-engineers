"""Check your team setup for exercise 210-08.

    python3 check.py [project folder]      (default: project)

Looks at the folder the way a teammate gets it from git: project notes, shared settings, a hook that stops the
protected workspace orders-prod, an MCP server file, one skill, and no file that contains anything that looks like
a token. Standard library only; nothing is sent anywhere.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

here = pathlib.Path(__file__).resolve().parent
project = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "project").resolve()
ok = True
n = 0


def say(good, label, why=""):
    global ok, n
    ok &= bool(good)
    n += 1
    print(f"[{'OK' if good else 'FAIL'}] {n} {label}" + ("" if good or not why else f": {why}"))


def load(rel):
    try:
        return json.loads((project / rel).read_text(encoding="utf-8")), ""
    except OSError:
        return None, f"{rel} not found"
    except ValueError as e:
        return None, f"{rel} is not valid JSON ({e})"


# 1 project notes
md = project / "CLAUDE.md"
lines = md.read_text(encoding="utf-8").splitlines() if md.is_file() else []
say(md.is_file() and 0 < len(lines) < 200, "CLAUDE.md present, under 200 lines",
    "missing" if not md.is_file() else f"{len(lines)} lines")

# 2 personal settings stay out of git
gi = project / ".gitignore"
ign = gi.read_text(encoding="utf-8").splitlines() if gi.is_file() else []
say(any(l.strip().lstrip("/") in (".claude/settings.local.json", ".claude/*.local.json") for l in ign),
    ".gitignore keeps .claude/settings.local.json out of git", "add .claude/settings.local.json to .gitignore")

# 3 shared settings: rules and the hook registration
settings, err = load(".claude/settings.json")
if settings is None:
    say(False, ".claude/settings.json has allow and deny rules", err)
    say(False, "hook registered under PreToolUse for Bash and MCP, path from $CLAUDE_PROJECT_DIR, onFailure block", err)
else:
    perms = settings.get("permissions", {})
    say(bool(perms.get("allow")) and bool(perms.get("deny")), ".claude/settings.json has allow and deny rules",
        "both lists need at least one rule")
    entries = settings.get("hooks", {}).get("PreToolUse", [])
    good = [e for e in entries
            if all(re.search(e.get("matcher", ""), t) for t in ("Bash", "mcp__fabric-core__list_items"))
            and any("CLAUDE_PROJECT_DIR" in h.get("command", "") and h.get("onFailure") == "block"
                    for h in e.get("hooks", []))]
    say(bool(good), "hook registered under PreToolUse for Bash and MCP, path from $CLAUDE_PROJECT_DIR, onFailure block",
        "matcher must match Bash and mcp__…, the command must start the hook through $CLAUDE_PROJECT_DIR")

# 4 the hook stops a sample call
hook = project / ".claude" / "hooks" / "block_protected.py"


def run(name):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    r = subprocess.run([sys.executable, str(hook)], input=(here / "events" / name).read_text(), text=True,
                       capture_output=True, env=env, timeout=30)
    return r.returncode, r.stderr.strip()


for name, want, label in (("prod.json", 2, "hook stops fab job run on orders-prod"),
                          ("mcp-prod.json", 2, "hook stops an MCP call on orders-prod"),
                          ("dev.json", 0, "hook lets orders-dev through")):
    if not hook.is_file():
        say(False, label, ".claude/hooks/block_protected.py not found")
    else:
        got, why = run(name)
        say(got == want and (want == 0 or why), label,
            f"exit {got}, expected {want}" + ("" if want == 0 else " and a reason on stderr"))

# 5 MCP server file
mcp, err = load(".mcp.json")
servers = (mcp or {}).get("mcpServers", {})
say(bool(servers) and all(s.get("url") or s.get("command") for s in servers.values()),
    ".mcp.json names at least one server with a url or command", err or "add mcpServers with one server")

# 6 one skill
skills = sorted((project / ".claude" / "skills").glob("*/SKILL.md"))
front = [s for s in skills if re.search(r"(?s)^---\s*\n.*?^name:\s*\S.*?^description:\s*\S.*?^---", s.read_text(encoding="utf-8"), re.M)]
say(bool(front), "a skill in .claude/skills/<name>/SKILL.md with name and description",
    "found none" if not skills else "frontmatter needs name: and description:")

# 7 no token in any file
PATTERNS = [
    (r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+", "JWT"),
    (r"(?i)bearer\s+(?!\$\{)[A-Za-z0-9._~+/-]{20,}", "bearer token"),
    (r"[A-Za-z0-9_~.-]{3}\dQ~[A-Za-z0-9_~.-]{31,34}", "Entra client secret"),
    (r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{30,}", "GitHub token"),
    (r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}", "API key"),
    (r"(?i)\"?(?:client_?secret|password|api_?key|access_?token)\"?\s*[:=]\s*\"?(?!\$\{)[^\s\"]{12,}", "secret value"),
]
hits = []
for f in sorted(project.rglob("*")):
    if not f.is_file() or ".git" in f.relative_to(project).parts:
        continue
    try:
        text = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for pat, kind in PATTERNS:
        if re.search(pat, text):
            hits.append(f"{f.relative_to(project)} ({kind})")
            break
say(not hits, "0 token patterns in any file", ", ".join(hits))

print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
