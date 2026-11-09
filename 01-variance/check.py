"""Check your result of exercise 1.

    python3 check.py --project <project folder> --first <the first weekend.py you moved out>
"""
import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

DATA = {
    "bikes-2025-09.csv": "502b831bda2bc5f1aceb1467ca5aebee5136b86c824d754557b17e42e502f246",
    "counters.csv": "c0a7a81ba996e67edd263a1a0b56b5bb8c4196d1e398fab5ce3b39f189df9a64",
}
SOLUTION_PERCENT = -28.3   # the percentage with the decisions in solution/prompt-2.md

results = []


def check(ok, label, reason=""):
    results.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'}  {label}" + ("" if ok or not reason else f": {reason}"))


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def digits(text):
    """'61,677', '61 677', '61’677' and '61677' all become '61677'."""
    return re.sub(r"(?<=\d)[,  ’'](?=\d{3}\b)", "", text)


def numbers(text):
    return [float(x) for x in re.findall(r"[-−+]?\d+(?:\.\d+)?", digits(text).replace("−", "-"))]


def check_data(project):
    for name, digest in DATA.items():
        path = project / name
        same = path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest
        check(same, f"{name} unchanged", "the data file is missing or was changed; run setup.py into a new folder")


def check_mythenquai(project):
    text = read(project / "results" / "mythenquai.md")
    check(text is not None, "results/mythenquai.md exists", "do step 2")
    if text is None:
        return
    flat = digits(text)
    if "60443" in flat and "61677" not in flat:
        check(False, "results/mythenquai.md: monthly total",
              "60,443 is the total with the correction factor; the prompt asks for raw counts")
    else:
        check("61677" in flat, "results/mythenquai.md: monthly total",
              "the September total isn't there; compare it with what a good result looks like")
    day = re.search(r"\b20(st|th)?\s+Sep|Sep\w*\.?\s+20\b|09-20|20\.\s?0?9\.|20/0?9", text, re.I)
    check("3586" in flat and day is not None, "results/mythenquai.md: busiest day and count",
          "the busiest day (date and count) isn't there")
    check(len([line for line in text.splitlines() if line.strip()]) <= 10, "results/mythenquai.md: at most ten lines",
          "the prompt allows at most ten lines")


def check_two_answers(project):
    text = read(project / "results" / "two-answers.md")
    check(text is not None, "results/two-answers.md exists", "do step 3")
    if text is None:
        return
    percents = re.findall(r"[-−+]?\d+(?:\.\d+)?\s*%", text)
    check(len(percents) >= 2, "results/two-answers.md: two numbers", "write down the percentage of each run")
    items = [line for line in text.splitlines() if re.match(r"\s*([-*]|\d+\.)\s+\S", line)]
    check(len(items) >= 2, "results/two-answers.md: decisions", "list at least two decisions from Claude's lists")


def check_prompt2(project):
    text = read(project / "prompt-2.md")
    check(text is not None, "prompt-2.md exists", "do step 4")
    if text is None:
        return
    lines = [line for line in text.splitlines() if re.match(r"\s*([-*]|\d+\.)\s+\S", line)]
    check(len(lines) >= 3, "prompt-2.md: decisions, one per line", "write each decision on its own line, at least three")
    check(re.search(r"15\s*(\.|th)?\s*(Sep|9)|Sep\w*\.?\s*15|09-15", text, re.I) is not None,
          "prompt-2.md decides Monday 15 September", "say whether Monday 15 September counts as a weekday")
    check("weekend.py" in text, "prompt-2.md asks for weekend.py", "ask for a script weekend.py")


def run_script(script, project):
    """Run a copy inside the project, so a script that opens files next to itself finds the data too."""
    copy = project / f".check-{script.stem}.py"
    shutil.copyfile(script, copy)
    try:
        run = subprocess.run([sys.executable, str(copy)], cwd=project, capture_output=True, text=True, timeout=120)
    finally:
        copy.unlink()
    return run.returncode, run.stdout, run.stderr


def percentages(text):
    """Absolute value of every number followed by %: '-28.3 %', '28.3% fewer' and '−28.3%' all give 28.3."""
    return [abs(float(x)) for x in re.findall(r"[-−+]?(\d+(?:\.\d+)?)\s*%", digits(text))]


def decimals(text):
    """Every number written with a decimal point, so a year, a counter count or a day doesn't count."""
    return sorted(abs(float(x)) for x in re.findall(r"\d+\.\d+", digits(text)))


def check_scripts(project, first):
    second = project / "weekend.py"
    check(second.is_file(), "weekend.py in the project", "the second run should have written a new weekend.py")
    check(first is not None and first.is_file(), "the first weekend.py, moved out of the project",
          "pass the moved script with --first")
    if not (second.is_file() and first is not None and first.is_file()):
        return
    if first.resolve() == second.resolve():
        check(False, "two different scripts", "--first must be the script you moved out, not the new one")
        return
    outputs = []
    for script in (first, second):
        code, out, err = run_script(script, project)
        check(code == 0, f"{script.name} runs", (err.strip().splitlines() or ["no output"])[-1])
        outputs.append(out)
    if not all(outputs):
        return
    # the percentage: the last number with a % sign, or else the last number printed
    pct = [percentages(out) or [abs(x) for x in numbers(out)[-1:]] for out in outputs]
    check(bool(pct[0]) and bool(pct[1]), "both scripts print a percentage", "the script prints no number")
    if not (pct[0] and pct[1]):
        return
    same_pct = pct[0][-1] == pct[1][-1]
    same_dec = decimals(outputs[0]) == decimals(outputs[1])
    check(same_pct and same_dec, "both scripts print the same numbers",
          f"first: {decimals(outputs[0])} and {pct[0][-1]} %, second: {decimals(outputs[1])} and {pct[1][-1]} %; "
          "a decision is still open, add a line to prompt-2.md")
    if same_pct and same_dec:
        note = "the same as with the solution's decisions" if pct[1][-1] == abs(SOLUTION_PERCENT) else \
            f"the solution's decisions give {SOLUTION_PERCENT}; yours are different, which is fine"
        print(f"info  percentage {pct[1][-1]} % fewer or more: {note}")


def check_answer(project):
    text = read(project / "results" / "answer.md")
    check(text is not None, "results/answer.md exists", "do step 5")
    if text is None:
        return
    check(re.search(r"\bscript\b", text, re.I) is not None and re.search(r"\b(prompt|decid|decision)", text, re.I) is not None,
          "results/answer.md: your rule for numbers", "say where the decisions go and what computes the number")


def main():
    parser = argparse.ArgumentParser(description="Check your result of exercise 1.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--first", help="the first weekend.py, moved out of the project in step 4")
    args = parser.parse_args()
    project = pathlib.Path(args.project).expanduser().resolve()
    first = pathlib.Path(args.first).expanduser().resolve() if args.first else None
    if not project.is_dir():
        print(f"check: {project} is not a folder", file=sys.stderr)
        sys.exit(2)
    check_data(project)
    check_mythenquai(project)
    check_two_answers(project)
    check_prompt2(project)
    check_scripts(project, first)
    check_answer(project)
    failed = results.count(False)
    print("all checks passed" if not failed else f"{failed} of {len(results)} checks failed")
    sys.exit(0 if not failed else 1)


main()
