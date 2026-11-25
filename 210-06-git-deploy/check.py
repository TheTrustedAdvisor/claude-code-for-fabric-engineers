#!/usr/bin/env python3
"""Grades exercise 210-06-git-deploy.

    python3 check.py [repo folder]        # default repo/

Runs the dry run (dry_run.py) for the environment test, then greps everything it would publish for the dev IDs from
target.json. Passes when config.yml names the parameter file, every notebook is bound to lh_kurs of the test
workspace, and no dev ID is left anywhere. Standard library only; no Fabric, no sign-in.
"""
import json
import sys

sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from dry_run import dry_run  # noqa: E402


def main(argv):
    repo = (HERE / (argv[0] if argv else "repo")).resolve()
    out, binding, named, target = dry_run(repo, "test", quiet=True)
    dev = json.loads((HERE / "target.json").read_text())["dev"]
    dev_ids = {dev["workspace"]["id"]: f"dev workspace {dev['workspace']['name']}"}
    dev_ids.update({i: f"dev {t.lower()} {n}" for t, d in dev["items"].items() for n, i in d.items()})
    ok = True

    def say(good, text):
        nonlocal ok
        ok &= good
        print(f"[{'OK' if good else 'FAIL'}] {text}")

    say(named, "config.yml names the parameter file under core.parameter"
        + ("" if named else ": without it, fab deploy ignores parameter.yml"))
    lh, ws = target["items"]["Lakehouse"]["lh_kurs"], target["workspace"]["id"]
    for name, b in sorted(binding.items()):
        good = b.get("default_lakehouse") == lh and b.get("default_lakehouse_workspace_id") == ws
        stuck = dev_ids.get(b.get("default_lakehouse")) or dev_ids.get(b.get("default_lakehouse_workspace_id"))
        say(good, f"{name} bound to lh_kurs in the test workspace" if good else
            f"{name} still bound to dev" if stuck else f"{name} bound to something else")
    hits = []
    for f in sorted(out.rglob("*")):
        if f.is_file():
            text = f.read_text()
            hits += [(f.relative_to(out), label) for i, label in dev_ids.items() if i in text]
    for path, label in hits:
        print(f"       {path}: {label}")
    print(f"dev GUIDs found: {len(hits)}")
    ok &= not hits
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
