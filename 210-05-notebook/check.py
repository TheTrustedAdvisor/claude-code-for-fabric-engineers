#!/usr/bin/env python3
"""Grades exercise 210-05-notebook.

    python3 check.py [answers.json]                       # the local part: next actions and the open session
    python3 check.py [answers.json] --live -w <workspace id> -a <notebook id>
                                                          # optional part: fntk lists no active session for your notebook

Standard library only. The local part needs no Fabric capacity and no sign-in.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = json.loads((HERE / "transcript.json").read_text())


def norm(s):
    return " ".join(str(s or "").lower().replace("_", "-").split())


def step(n):
    return next(s for s in T["steps"] if s["step"] == n)


def grade(answer, want, wrong, hint_wrong, hint_empty):
    a = norm(answer)
    if not a:
        return False, hint_empty
    for w, h in wrong:
        if w in a:
            return False, h
    if all(x in a for x in want):
        return True, "right"
    return False, hint_wrong


def main(argv):
    args = [a for a in argv if not a.startswith("-")]
    path = Path(args[0]) if args and args[0].endswith(".json") else HERE / "answers.json"
    ans = json.loads(path.read_text())
    s1, s2 = step(1)["response"], step(2)["response"]
    sid, op = s1["data"]["session_id"], s2["data"]["op_id"]
    results = [
        ("Q1 session starting", *grade(ans.get("q1"), ["get-session", sid[:8]],
                                      [("start-session", "starting a second session: follow next_actions, poll the one you have")],
                                      "look at next_actions in step 1: which command, for which session?",
                                      "no answer")),
        ("Q2 code running", *grade(ans.get("q2"), ["get-result", op],
                                  [("code run", "submitting the code again: the response says it's running, poll get-result")],
                                  "look at next_actions in step 2: which command, with which execution id?",
                                  "no answer")),
        ("Q3 server stopped, session listed", *grade(ans.get("q3"), ["delete-session"],
                                                    [("server start", "the server was never the session: end the session itself")],
                                                    "the local stop ended nothing in Fabric: which command ends the session?",
                                                    "no answer")),
    ]
    right = sum(1 for _, ok, _ in results if ok)
    for name, ok, why in results:
        print(f"[{'OK' if ok else 'WRONG'}] {name}: {why}")
    print(f"{right} of 3 next actions right")
    livy = [v for v in step(3)["then_read_from_fabric"]["value"] if v["state"] == "InProgress"]
    want = livy[0]["livyId"]
    got = norm(ans.get("open_livy_session"))
    open_ok = len(got) >= 8 and want.startswith(got.split()[0][:36]) if got else False
    print(f"[{'OK' if open_ok else 'WRONG'}] open session: {'found ' + want if open_ok else 'which Livy session is still InProgress in step 3?'}")
    live_ok = True
    if "--live" in argv:
        try:
            ws, nb = argv[argv.index("-w") + 1], argv[argv.index("-a") + 1]
        except (ValueError, IndexError):
            sys.exit("--live needs -w <workspace id> -a <notebook id>")
        out = subprocess.run(["fntk", "notebook", "list-sessions", "-w", ws, "-a", nb, "--json"], capture_output=True, text=True)
        try:
            data = json.loads(out.stdout[out.stdout.index("{"):])["data"]
            sessions = data if isinstance(data, list) else next((data[k] for k in ("sessions", "items", "value") if k in data), [])
            closed = {"dead", "killed", "ended", "succeeded", "cancelled", "canceled", "failed", "error"}
            sessions = [x for x in sessions if norm(x.get("livy_session_state") or x.get("state") if isinstance(x, dict) else "") not in closed]
        except (ValueError, KeyError):
            sys.exit(f"could not read fntk's answer:\n{out.stdout[-800:]}{out.stderr[-800:]}")
        live_ok = not sessions
        print(f"[{'OK' if live_ok else 'WRONG'}] live: {'no active session' if live_ok else f'{len(sessions)} session(s) still open: end them and read back'}")
    ok = right == 3 and open_ok and live_ok
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
