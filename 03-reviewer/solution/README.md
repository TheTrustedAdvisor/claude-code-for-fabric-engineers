# Exercise 3: notes for instructors

What is fixed and what varies, step by step. Fixed parts are what `check.py` checks; varying parts are the model's behavior, which differs from run to run.

| Step | Fixed | Varies |
|---|---|---|
| 2 | Statements 1 to 4 cite a file, line or rule and are `G`; statement 5 cites nothing and is `U`. Statement 2 doesn't hold: M1 ends with "When the denominator is a constant, such as `/ 12`, use the `/` operator." and `Sales.tmdl:22` is `[Total Sales] / 12`. Statement 4 holds: `Margin %` (`Sales.tmdl:16-19`) has no `formatString`. | Which second statement people spot-check. |
| 3 | A sentence exists. | Whether it's right. A wrong first judgment is a good result to talk about, not a failure. |
| 4 | The reviewer runs in the background as `reviewer(…)`; `Ctrl+O` shows `Prompt:` below it. | What Claude adds to the task prompt. In the tests (Opus 5.5) the prompt carried a hint toward exceptions in the rules in three of five sessions that had discussed statement 2 first on Claude Code v2.1.318, and in none of six on v2.1.319; never the word "statement 2". In all eleven, Claude introduced the result as a confirmation ("The reviewer agrees with your judgment"), in eleven fresh sessions never. A session A without any hint is normal; the debrief point is that only the task prompt shows it, not the result. When the first judgment was clearly wrong (statement 4), Claude disagreed in the conversation and the task prompt carried nothing of it (2 of 2). |
| 5 | The prompt holds files, job and output format. | Wording. In eleven fresh sessions no prompt mentioned exceptions. |
| 6 | The quote is literally in a source file. | Which finding people pick. The reviewer found statement 2 wrong in all 24 test sessions, with and without a hint, so the planted error doesn't depend on session A. Some reports add matters of taste (abbreviations such as `LY` under M3). |
| 7 | keep 1, 3, 4; strike 2; 5 not a fact. | – |

## Questions for the debrief

- What did your task prompt in session A contain besides files and job, and would it have pushed a reviewer toward a result?
- How did Claude present the reviewer's result in session A, and in session B?
- Which finding did you check yourself, and what did the source say?
- Your first judgment against your final decision: what would you have released?

## Rescue

| Observation | What to do |
|---|---|
| After `@agent-reviewer` nothing seems to happen. | The reviewer runs in the background; Claude reports "Agent … finished" after about 20 seconds. If no `reviewer(…)` line appears, the mention was picked from the file suggestions or misspelled: type it in full. |
| `Ctrl+O` shows no `Prompt:`. | Scroll up in the transcript viewer to the `reviewer(…)` line. After `/clear` or in a new session, the call is gone. |
| Someone asks Claude what it told the reviewer. | The answer is written by the model; the prompt as passed stands unformatted in `Ctrl+O`. |
| The reviewer changed a file. | It can't with `tools: Read, Grep, Glob`. If `check.py` reports a changed file, it was edited by hand or by the main session; run setup again. |
| A statement marked `U` because it "sounds wrong". | `G` and `U` describe the citation, not the truth. Statement 2 is `G` and wrong. |

## Check the solution yourself

The files in this folder are one finished run: the filled-in notes `sign-off.example.md`. Put them into a fresh project and `check.py` prints "all checks passed"; on a fresh project without them, it fails. From the exercise folder, in Bash or Git Bash:

```
./setup.sh /var/tmp/03-solved --notes /var/tmp/03-solved-notes
cp solution/sign-off.example.md /var/tmp/03-solved-notes/sign-off.md
python3 check.py --project /var/tmp/03-solved --notes /var/tmp/03-solved-notes
```

Use new folders each time; setup refuses a folder that already exists.
