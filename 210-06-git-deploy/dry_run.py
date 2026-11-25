#!/usr/bin/env python3
"""Dry run of `fab deploy --config config.yml --target_env test` for exercise 210-06-git-deploy: no Fabric, no sign-in.

    python3 dry_run.py [repo folder] [--env test]

Does what fabric-cicd does with a parameter file before it publishes: reads config.yml, and only if config.yml names a
parameter file under core.parameter, applies its find_replace entries for the target environment. The tokens
$workspace.$id and $items.<type>.<name>.$id resolve to the IDs of the target workspace, taken from target.json (what a
deploy would find there). Writes the item definitions as they would be published into out/<env>/ and prints each
notebook's binding. Standard library only; reads the subset of YAML that config.yml and parameter.yml use here.
"""
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def yaml_lite(text):
    """Nested mappings and lists of mappings with scalar values, indentation by spaces, # comments. Enough for
    config.yml and parameter.yml of this exercise; for anything else use a real YAML parser."""
    lines = []
    for raw in text.splitlines():
        line = re.sub(r"\s+#.*$", "", raw.rstrip()) if not raw.lstrip().startswith("#") else ""
        if line.strip():
            lines.append((len(line) - len(line.lstrip()), line.strip()))

    def scalar(v):
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            return v[1:-1]
        if v.startswith("[") and v.endswith("]"):
            return [scalar(x) for x in v[1:-1].split(",") if x.strip()]
        return {"true": True, "false": False}.get(v.lower(), v)

    def block(i, indent):
        if i < len(lines) and lines[i][1].startswith("- "):
            out = []
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
                ind, txt = lines[i]
                lines[i] = (ind + 2, txt[2:])
                item, i = block(i, ind + 2)
                out.append(item)
            return out, i
        out = {}
        while i < len(lines) and lines[i][0] == indent:
            key, _, val = lines[i][1].partition(":")
            if val.strip():
                out[key.strip()] = scalar(val)
                i += 1
            elif i + 1 < len(lines) and lines[i + 1][0] > indent:
                out[key.strip()], i = block(i + 1, lines[i + 1][0])
            else:
                out[key.strip()] = None
                i += 1
        return out, i

    return block(0, lines[0][0])[0] if lines else {}


def resolve(token, target):
    def one(m):
        t = m.group(0)
        if t == "$workspace.$id":
            return target["workspace"]["id"]
        if t == "$workspace.$name":
            return target["workspace"]["name"]
        _, typ, name, prop = t.split(".")
        if prop != "$id":
            sys.exit(f"dry run: only $id is supported here, not {t}")
        try:
            return target["items"][typ][name]
        except KeyError:
            sys.exit(f"dry run: {t}: no {typ} named {name} in the target workspace")
    return re.sub(r"\$workspace\.\$(id|name)|\$items\.[A-Za-z]+\.[^.\s\"']+\.\$[a-z]+", one, token)


def items(repo):
    for plat in sorted(repo.glob("*/.platform")):
        meta = json.loads(plat.read_text())["metadata"]
        yield plat.parent, meta["type"], meta["displayName"]


def binding(text):
    m = re.search(r"^# META \{.*?^# META \}", text, re.S | re.M)
    if not m:
        return {}
    meta = json.loads("\n".join(l[6:] for l in m.group(0).splitlines()))
    return meta.get("dependencies", {}).get("lakehouse", {})


def dry_run(repo, env, quiet=False):
    target = json.loads((HERE / "target.json").read_text())[env]
    cfg = yaml_lite((repo / "config.yml").read_text())
    core = cfg.get("core") or {}
    ws = core.get("workspace")
    ws = ws.get(env) if isinstance(ws, dict) else ws
    if ws != target["workspace"]["name"]:
        sys.exit(f"dry run: config.yml targets {ws!r} for {env}, target.json describes {target['workspace']['name']!r}")
    pfile = core.get("parameter")
    pfile = pfile.get(env) if isinstance(pfile, dict) else pfile
    rules = []
    if pfile:
        p = (repo / pfile).resolve()
        if not p.exists():
            sys.exit(f"dry run: config.yml names {pfile}, which doesn't exist")
        rules = yaml_lite(p.read_text()).get("find_replace") or []
    out = HERE / "out" / env
    if out.exists():
        shutil.rmtree(out)
    say = (lambda *a: None) if quiet else print
    say(f"deploy {repo.name}/ to {ws} ({env}), parameter file: {pfile or 'none (config.yml has no core.parameter)'}")
    result = {}
    for folder, typ, name in items(repo):
        dst = out / folder.name
        shutil.copytree(folder, dst)
        for f in dst.rglob("*"):
            if not f.is_file() or f.name == ".platform":
                continue
            text = f.read_text()
            for r in rules:
                if r.get("item_type") and typ not in (r["item_type"] if isinstance(r["item_type"], list) else [r["item_type"]]):
                    continue
                if r.get("item_name") and name not in (r["item_name"] if isinstance(r["item_name"], list) else [r["item_name"]]):
                    continue
                rv = (r.get("replace_value") or {})
                new = rv.get(env, rv.get("_ALL_"))
                if new is not None and r.get("find_value"):
                    text = text.replace(str(r["find_value"]), resolve(str(new), target))
            f.write_text(text)
            if typ == "Notebook" and f.name.startswith("notebook-content"):
                result[name] = binding(text)
        say(f"  {typ:<9} {name}")
    for name, b in result.items():
        say(f"  {name}: default_lakehouse {b.get('default_lakehouse')}, workspace {b.get('default_lakehouse_workspace_id')}")
    say(f"written to {out.relative_to(HERE)}/")
    return out, result, bool(pfile), target


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    env = sys.argv[sys.argv.index("--env") + 1] if "--env" in sys.argv else "test"
    args = [a for a in args if a != env]
    dry_run((HERE / (args[0] if args else "repo")).resolve(), env)
