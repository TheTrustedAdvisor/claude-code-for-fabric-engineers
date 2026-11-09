"""Check your result of exercise 2.

    python3 check.py --project <project folder> --notes <notes folder>
"""
import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
GUIDELINES = HERE / "team" / "modeling-guidelines.md"
RULE_ID = re.compile(r"\b(M[1-9][0-9]?)\b")
REF = re.compile(r"([\w-]+\.tmdl):(\d+)")
DECLARATION = re.compile(r"^\s*(table|measure|column|relationship|partition|expression|model|database)\b\s*(.*?)\s*(=.*)?$")
# What the team's guidelines find in the starter model: rule ID, file, object.
EXPECTED = {
    ("M2", "Sales.tmdl", "measure 'Margin %'"),
}

results = []


def check(ok, label, reason=""):
    results.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'}  {label}" + ("" if ok or not reason else f": {reason}"))
    return ok


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def object_maps(project):
    """For each .tmdl file: line number -> the object declared at or above that line."""
    maps = {}
    for path in sorted((project / "Sales.SemanticModel" / "definition").rglob("*.tmdl")):
        current, lines, pending = "", {}, []
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if line.strip().startswith("///"):
                pending.append(number)  # a description belongs to the object below it
                continue
            match = DECLARATION.match(line)
            if match:
                current = f"{match.group(1)} {match.group(2)}".strip()
            for waiting in pending:
                lines[waiting] = current
            pending = []
            lines[number] = current
        maps[path.name] = lines
    return maps


def findings(text, maps, skip_holds=True):
    """Set of (rule ID or None, file, object) cited in a review."""
    found = set()
    lines = text.splitlines()
    items = [line for line in lines if re.match(r"^\s*([-*+]|\d+[.)])\s", line)]
    for line in (items or lines):  # list items if there are any; prose such as "rules that hold" doesn't count
        negated = r"\b(not a violation|no violation|doesn't break|does not break)\b"
        holds = re.search(r"\b(allowed|allows|passes|complies)\b", line, re.I) or re.search(negated, line, re.I)
        rest = re.sub(negated, "", line, flags=re.I)
        breaks = re.search(r"\b(break|breaks|violat\w*|missing|has no|lacks|instead of|not allowed|must|should|change|add|replace)\b", rest, re.I)
        if skip_holds and holds and not breaks:
            continue  # a line that only says a rule holds is not a finding
        refs = REF.findall(line)
        if not refs:
            continue
        ids = RULE_ID.findall(line)
        if len(ids) == len(refs):
            pairs = zip(ids, refs)
        else:
            pairs = [(ids[0] if len(ids) == 1 else None, ref) for ref in refs]
        for rule, (name, number) in pairs:
            obj = maps.get(name, {}).get(int(number), "?")
            found.add((rule, name, obj))
    return found


def describe(items):
    return "; ".join(f"{rule or 'no rule ID'} at {name}, {obj}" for rule, name, obj in sorted(items, key=str))


def rule_lines(text):
    return {m.group(1): line.strip() for line in text.splitlines()
            if (m := re.match(r"^\s*-\s*\*\*(M[1-9][0-9]?)\b", line))}


def section(text, heading_start):
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].lower().startswith(heading_start)
            continue
        if inside:
            lines.append(line)
    return "\n".join(lines)


def filled(text, label):
    match = re.search(rf"^-[ \t]*{re.escape(label)}:[ \t]*(\S.*)$", text, re.M)
    return match.group(1).strip() if match else ""


def main():
    parser = argparse.ArgumentParser(description="Check your result of exercise 2.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--notes", required=True)
    args = parser.parse_args()
    project = pathlib.Path(args.project).expanduser().resolve()
    notes_dir = pathlib.Path(args.notes).expanduser().resolve()

    if not (project / "Sales.SemanticModel" / "definition").is_dir():
        print(f"FAIL  no Sales.SemanticModel/definition in {project}; is --project the folder you created with setup.sh?")
        sys.exit(1)
    maps = object_maps(project)
    original = GUIDELINES.read_text(encoding="utf-8")

    # Step 2: the review without guidelines
    without = read(project / "reviews" / "without.md")
    if check(without is not None, "reviews/without.md exists", "run step 2 and let Claude write the file"):
        count = len({(name, obj) for _, name, obj in findings(without, maps, skip_holds=False)})
        check(count >= 5, f"reviews/without.md: {count} distinct places cited with file:line",
              "expected five or more; did the prompt ask for file:line?")

    # Step 4: the review against the guidelines
    copied = read(project / "modeling-guidelines.md")
    check(copied is not None, "modeling-guidelines.md is in the project", "copy team/modeling-guidelines.md (step 4)")
    if copied is not None:
        check(copied.replace("\r\n", "\n") == original, "modeling-guidelines.md is unchanged",
              "it differs from team/modeling-guidelines.md; change only your copy modeling-guidelines-b.md (step 5)")
    with_text = read(project / "reviews" / "with.md")
    if check(with_text is not None, "reviews/with.md exists", "run step 4 and let Claude write the file"):
        with_found = findings(with_text, maps)
        missing, extra = EXPECTED - with_found, with_found - EXPECTED
        check(not missing, "reviews/with.md finds the violation of M2",
              f"missing: {describe(missing)}. Look at that line yourself: is it a violation of the rule?")
        check(not extra, "reviews/with.md reports nothing else",
              f"also reported: {describe(extra)}. Open the file at that line and the rule it cites, "
              "and read the rule to the end: does it really say that?")

    # Step 5: one line changed
    changed_text = read(project / "modeling-guidelines-b.md")
    changed_rule = None
    if check(changed_text is not None, "modeling-guidelines-b.md exists",
             "copy the guidelines to modeling-guidelines-b.md and change one line (step 5)"):
        old = original.rstrip("\n").splitlines()
        new = changed_text.replace("\r\n", "\n").rstrip("\n").splitlines()
        changed = [i for i, (a, b) in enumerate(zip(old, new)) if a.strip() != b.strip()]
        diff = []
        if len(old) == len(new) and len(changed) == 1:
            before, after = rule_lines(old[changed[0]]), rule_lines(new[changed[0]])
            if before and before.keys() == after.keys():
                diff = list(before)
        if check(len(diff) == 1, "modeling-guidelines-b.md: exactly one rule line changed",
                 f"{len(changed)} lines differ from the original; change the text of one rule line, keep its ID "
                 "and leave every other line as it is"):
            changed_rule = diff[0]
    with_b = read(project / "reviews" / "with-b.md")
    if check(with_b is not None, "reviews/with-b.md exists", "run the review against modeling-guidelines-b.md (step 5)") and changed_rule:
        found_b = findings(with_b, maps)
        delta = found_b ^ EXPECTED
        others = {item for item in delta if item[0] != changed_rule}
        if not delta:
            hint = (f"the result is the same as in step 4. Your new {changed_rule} doesn't change what any measure "
                    "violates; pick a change that affects exactly one measure")
        else:
            hint = (f"compared with step 4, {len(delta)} findings changed: {describe(delta)}. "
                    "Claude applies the changed line as written. Reword it so it says only what you mean, then run step 5 again")
        check(len(delta) == 1 and not others, f"reviews/with-b.md: exactly one finding changed, under {changed_rule}", hint)

    # Notes
    notes = read(notes_dir / "notes.md")
    if check(notes is not None, "notes.md exists", f"no notes.md in {notes_dir}"):
        s2, s3, s4 = section(notes, "step 2"), section(notes, "step 3"), section(notes, "step 4")
        s5, s6 = section(notes, "step 5"), section(notes, "step 6")
        check(bool(re.search(r"\d", filled(s2, "Number of findings"))), "notes, step 2: number of findings")
        check(bool(re.search(r"\d", filled(s2, "Messages in /context after the review"))), "notes, step 2: Messages from /context")
        prediction = [line for line in s3.splitlines() if line.strip().startswith("-") and len(line.strip()) > 2]
        check(bool(prediction), "notes, step 3: your prediction", "write it before step 4")
        check(bool(re.search(r"\d", filled(s4, "Number of findings"))), "notes, step 4: number of findings")
        rule_note = filled(s5, "Rule ID you change")
        check(bool(rule_note) and (changed_rule is None or changed_rule in rule_note),
              "notes, step 5: the rule you changed", f"write the rule ID{' ' + changed_rule if changed_rule else ''}")
        check(bool(filled(s5, "The finding you expect to appear or drop (file:line)")), "notes, step 5: the finding you expected to change")
        sentence = [line for line in s6.splitlines() if line.strip() and not line.startswith("One sentence")]
        check(bool(sentence), "notes, step 6: your sentence")

    if all(results):
        print("all checks passed")
    else:
        print(f"{results.count(False)} of {len(results)} checks failed")
        sys.exit(1)


main()
