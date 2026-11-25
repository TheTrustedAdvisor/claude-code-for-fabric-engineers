#!/usr/bin/env python3
"""Grades exercise 210-07-tmdl.

    python3 check.py [project folder]        # default project/

Two checks, like in the video. The diff: every file of the model is compared with base/ (the model as exported), and
only definition/tables/orders.tmdl may differ. The number: a small evaluator reads the measure 'Total Revenue' from
orders.tmdl, maps each column to its sourceColumn, computes the measure per region over seed/orders.csv (the same
1,000 rows as the lab, seed 210) and compares it with the expected totals, which come from the seed, not from the
model. The evaluator knows SUM(<table>[<column>]) only; that is all the task needs. Standard library only.
"""
import csv
import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = "sm_kurs.SemanticModel"
EXPECTED = {"East": 54901.63, "North": 68531.33, "South": 66766.59, "West": 61999.88}   # SUM(amount) per region


def files(root):
    return {p.relative_to(root).as_posix(): p.read_text() for p in sorted(root.rglob("*")) if p.is_file()}


def name(raw):
    raw = raw.strip()
    return raw[1:-1].replace("''", "'") if raw.startswith("'") and raw.endswith("'") else raw


def parse_table(text):
    """Columns {name: sourceColumn} and measures {name: (expression, formatString)} of one TMDL table file."""
    cols, measures, cur = {}, {}, None
    for line in text.splitlines():
        m = re.match(r"^\tcolumn (.+?)\s*$", line)
        if m:
            cur = ("column", name(m.group(1)))
            cols[cur[1]] = None
            continue
        m = re.match(r"^\tmeasure (.+?)\s*=\s*(.*)$", line)
        if m:
            cur = ("measure", name(m.group(1)))
            measures[cur[1]] = [m.group(2).strip(), None]
            continue
        if re.match(r"^\t\S", line):
            cur = None
            continue
        m = re.match(r"^\t\t(sourceColumn|formatString):\s*(.+?)\s*$", line)
        if m and cur:
            if cur[0] == "column" and m.group(1) == "sourceColumn":
                cols[cur[1]] = m.group(2)
            elif cur[0] == "measure" and m.group(1) == "formatString":
                measures[cur[1]][1] = m.group(2)
    return cols, measures


def evaluate(expr, cols):
    """SUM(orders[col]) per region over the seed, or an error text."""
    m = re.fullmatch(r"SUM\s*\(\s*'?orders'?\s*\[(.+?)\]\s*\)", expr.strip(), re.I)
    if not m:
        return None, f"the evaluator only knows SUM(orders[<column>]), got: {expr}"
    col = m.group(1)
    if col not in cols:
        return None, f"[{col}] is no column of orders (columns: {', '.join(cols)})"
    src = cols[col]
    out = {}
    with open(HERE / "seed/orders.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            if src not in row:
                return None, f"sourceColumn {src} of [{col}] is not in the lakehouse table"
            out[row["region"]] = out.get(row["region"], 0.0) + float(row[src])
    return {k: round(v, 2) for k, v in out.items()}, None


def main(argv):
    proj = (HERE / (argv[0] if argv else "project")).resolve()
    ok = True

    def say(good, text):
        nonlocal ok
        ok &= good
        print(f"[{'OK' if good else 'FAIL'}] {text}")

    if not (proj / MODEL).is_dir():
        print(f"no {MODEL}/ in {proj}")
        return 1
    base, now = files(HERE / "base" / MODEL), files(proj / MODEL)
    changed = sorted(k for k in set(base) | set(now) if base.get(k) != now.get(k))
    say(changed == ["definition/tables/orders.tmdl"],
        "the diff touches only definition/tables/orders.tmdl" if changed == ["definition/tables/orders.tmdl"]
        else f"changed files: {', '.join(changed) or 'none'}")
    cols, measures = parse_table(now.get("definition/tables/orders.tmdl", ""))
    renamed = "Sales Amount" in cols and "amount" not in cols
    say(renamed and cols.get("Sales Amount") == "amount",
        "column 'Sales Amount' reads sourceColumn amount" if renamed and cols.get("Sales Amount") == "amount"
        else "rename missing: expected column 'Sales Amount' with sourceColumn: amount, and no column amount"
        if not renamed else f"column 'Sales Amount' reads sourceColumn {cols.get('Sales Amount')}, the lakehouse "
                            "table has amount")
    m = measures.get("Total Revenue")
    if not m:
        say(False, "measure 'Total Revenue' missing in the table orders")
    else:
        say(m[1] == "#,0.00", f"measure 'Total Revenue' = {m[0]}, formatString {m[1]}")
        got, err = evaluate(m[0], cols)
        if err:
            say(False, err)
        else:
            for region, want in EXPECTED.items():
                g = got.get(region)
                good = g is not None and abs(g - want) <= 0.01
                ok &= good
                print(f"{region:<6} {g if g is not None else '-':>9} {'=' if good else '!='} {want:.2f}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
