# Exercise 7: notes for teachers

Expected results per step, and what varies. The participant's checklist is "What a good result looks like" in `../README.md`; this page adds what you see when you run it yourself. Tested with Claude Code v2.1.318 (Linux), Opus 5.5, auto mode, in two runs (author, independent reviewer).

Example files from the test run, all from real sessions:

- `handoff-note-day-one.md`: the note at the end of step 6 (Claude's draft from step 3, plus the finding added by hand, with the open question and the next step made to agree).
- `handoff-note.md`: the same note after step 7, updated by the morning session.
- `cold-start.md`: the four items as a participant would write them.

| Step | Fixed result (Claude Code or the files decide) | Varies (the model decides) |
|---|---|---|
| 2 | `Session renamed to: sales-migration`; the name on the prompt bar | – |
| 3 | `handoff-note.md` filled in, four sections | wording and length (19 or 20 lines in the tests); whether Claude flags citations it took from `migration.md` without opening the logs |
| 4, test 1 | – | no number in any test run ("The note doesn't give a number. This is still the open question"); first file `config/source.yaml`; the statement it wouldn't take over varies: the error text without a log citation, "Gateway ruled out", or the uncommitted state of the note |
| 5 | – | "At most 16 copies at once", 48 / 3 = 16 with lines from `config/source.yaml`; once also the Sunday maintenance window |
| 5, after the answer | – | Claude may offer to add the finding to the note ("I can add this to handoff-note.md if you'd like.", test run 2) and Claude Code may pre-fill an acceptance in the prompt field; accepting it spoils test 2 |
| 4, test 2 | – | still no number ("The note doesn't say"), in every test run |
| 6, test 3 | – | names 16 and opens `pipeline-content.json` first; distrusts the limit if the note still says `config/source.yaml` hasn't been read (seen once, see below) |
| 7 | `/resume` lists `sales-migration`; the morning session isn't named | finds the missing `batchCount` (ADF had 8), explains the 4 failures with the default of 20, proposes a value and asks before editing (yes/no in run 1, "which value you want" in run 2) |
| 9 | `all checks passed` | – |

## What participants get stuck on

- **"Read only migration.md" in step 3:** with that wording, Claude refused to open the template and showed the note in the chat (test run 1). The prompt in the README names both files.
- **A note that contradicts itself:** participants add the number under "State" and leave "Next step: read config/source.yaml, not read yet". The fresh session then refuses the number: "It cites config/source.yaml:7-12 … Yet line 20 says neither that file nor pipeline-content.json has been read. So the citation can't come from actually reading the file." That's the point of step 6: the note has to agree with itself. `check.py` reports it.
- **Writing a claim you didn't check:** in test run 1, the note got "The ForEach has no batch count" added by hand before anyone had opened the pipeline. The fresh session flagged it as a claim about an unread file.
- **The fresh session doesn't trust everything:** that's intended. It separates what the last session read itself from what the note only passes on from `migration.md`.
- **Auto memory:** in all three test runs, Claude saved nothing to auto memory, so the fresh sessions knew only the note. If a participant's test 2 names 16 anyway, have them run `/memory` and look at the auto memory folder.
- **`claude -p` and `/resume`:** the cold-start sessions don't appear in `/resume`. Participants who look for them there won't find them; they're not meant to.
- **Windows:** not tested for this exercise. The commands are the same as in exercise 5; start Claude Code from PowerShell or Windows Terminal.

## Check the solution yourself

The files in this folder are one finished run: `handoff-note.md`, `cold-start.md` and the pipeline with `batchCount` 8 from step 7. Put them into a fresh project and `check.py` prints "all checks passed"; on a fresh project without them, it fails. From the exercise folder, in Bash or Git Bash:

```
./setup.sh /var/tmp/07-solved
cp solution/handoff-note.md solution/cold-start.md /var/tmp/07-solved/
cp -r solution/workspace/. /var/tmp/07-solved/workspace/
python3 check.py --project /var/tmp/07-solved
```

Use new folders each time; setup refuses a folder that already exists.
