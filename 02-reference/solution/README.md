# Exercise 2: notes for teachers

Expected results per step, and what varies. The participant's checklist is "What a good result looks like" in `../README.md`; this page adds what you see when you run it yourself. Tested with Claude Code v2.1.318 (Linux) and Opus 5.5. The files of one full run are in `example-run/`. Model and guidelines are the same files as in exercise 3 (`03-reviewer/`).

| Step | Fixed result (the files decide) | Varies (the model decides) |
|---|---|---|
| 2 | – | 8 to 13 findings in eight runs (four in manual mode on v2.1.318, four in auto mode on v2.1.319: 8, 9, 11, 9); always `Margin %` without a format string, `Avg Monthly Sales` divides by a fixed 12, no month column, `Amount` and `Cost` visible, `OrderDate` visible, `discourageImplicitMeasures` or a time part in `OrderDate`, hard-coded data source; in manual-mode runs also amounts without currency and the all-zero `logicalId` in `.platform`; once also "the `/` operator is used instead of `DIVIDE`" |
| 4 | exactly one finding: M2 at `Sales.tmdl:17` (`Margin %`, no `formatString`) | whether Claude lists the rules that hold; it usually names the M1 exception for `/ 12` |
| 4, `/context` | – | Messages 14.3k after step 2 and 8.7k after step 4 in the test run |
| 5 | with M1 cut after "instead of an error.": M2 stays, M1 at `Sales.tmdl:22` is new, Claude adds "It still breaks the rule as written." | – |
| 8 | `all checks passed` | – |

## What participants get stuck on

- **The guidelines are in the project before step 2.** Then the first review may read them on its own (not tested) and the comparison is gone. The setup leaves them out; step 4 copies them in. If someone did it too early: delete `modeling-guidelines.md` from the project, `/clear`, run step 2 again.
- **The fixed 12 drops out in step 4.** Both reviews without guidelines in the tests said that `Avg Monthly Sales` is wrong for any filter that isn't a full year; against the guidelines, it's not on the list, because no rule covers it. That's correct for the task and worth a word: the guidelines decide what counts as a violation, not whether the numbers are right. Exercise 3 picks this up.
- **Step 5 changes nothing,** for example a change to M3 or M4. `check.py` says so; pick a rule that touches exactly one measure.
- **Step 5 changes more than one line,** or edits `modeling-guidelines.md` instead of the `-b` copy. `check.py` reports both.
- **Permission prompts:** in auto mode there are none here. Claude often reads the files with a shell loop (`cat -n`); in manual mode that asks each time, and "1. Yes" is fine, the command only reads.

## Check the solution yourself

The files in this folder are one finished run: the three reviews, both guideline files and the notes from `example-run/`. Put them into a fresh project and `check.py` prints "all checks passed"; on a fresh project without them, it fails. From the exercise folder, in Bash or Git Bash:

```
./setup.sh /var/tmp/02-solved --notes /var/tmp/02-solved-notes
cp solution/example-run/without.md solution/example-run/with.md solution/example-run/with-b.md /var/tmp/02-solved/reviews/
cp team/modeling-guidelines.md solution/example-run/modeling-guidelines-b.md /var/tmp/02-solved/
cp solution/example-run/notes.md /var/tmp/02-solved-notes/
python3 check.py --project /var/tmp/02-solved --notes /var/tmp/02-solved-notes
```

Use new folders each time; setup refuses a folder that already exists.
