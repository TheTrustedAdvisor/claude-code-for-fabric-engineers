# Exercise 3: Who checks the reviewer?

Companion exercise to video 3, "Reviewer subagents: who checks Claude's work in Fabric?". About 30 minutes. Everything runs locally on TMDL files; no Fabric capacity needed. Only the optional step 8 uses your own semantic model.

## Scenario

- **Role:** You're a BI developer on a team that keeps its Fabric semantic models in Git.
- **Situation:** Your colleague Jonas reviewed the measures of the Sales semantic model against the team's `modeling-guidelines.md`. His review says "ready to release after two fixes". Before anyone applies those fixes, you sign the review off. One of his statements doesn't hold.
- **Task:** Judge the review yourself first, then have a reviewer subagent check it, look at what Claude told that reviewer, check one finding at the source, and decide.
- **Tools:** a reviewer subagent in `.claude/agents/reviewer.md`, `@agent-reviewer`, `Ctrl+O` (transcript viewer), `/exit`, a second terminal, your editor.

## Before you start

- Claude Code installed and signed in. Python 3 as `python3` (check with `python3 --version`) and Git.
  - **macOS, Linux, WSL:** use your normal terminal.
  - **Windows:** start Claude Code from PowerShell or Windows Terminal and use Git Bash for the other commands; in PowerShell, `python3 setup.py …` does the same as `./setup.sh …`.
- Open a second terminal. Run the setup and the check there.
- Create the project outside your own projects and outside any folder that has a `CLAUDE.md` above it: Claude Code also loads `CLAUDE.md` files from every folder above the one you start in. The examples use `/var/tmp`; on Windows use a folder in your user profile, for example `~/work/03-reviewer`. The setup script refuses a folder inside a Git repository or below a `CLAUDE.md`.
- Keep your notes **outside** the project, for example in `/var/tmp/03-notes`. The reviewer can read every file in the project, your notes included.
- The reviewer loads the same `CLAUDE.md` files as your main session, including your personal `~/.claude/CLAUDE.md`. If yours holds review habits, they reach the reviewer too; for this exercise, a personal file without such rules gives the clearest result.

In the second terminal, from this folder (`03-reviewer/` in the companion repo):

```
./setup.sh /var/tmp/03-reviewer --notes /var/tmp/03-notes
```

It creates the project as a Git repository with one commit, and `sign-off.md` in the notes folder.

**Permission mode:** the project sets no mode, so Claude Code starts in its default, auto mode (Claude Code v2.1.283 or later; the status line shows "⏵⏵ auto mode on"). The reviewer has only reading tools, and nothing in this exercise needs a yes. If your organization turned auto mode off, Claude Code starts in manual mode: then read each permission prompt and choose "1. Yes" only for read-only commands.

## What's in the project

| Path | What it is |
|---|---|
| `Sales.SemanticModel/` | A small Sales semantic model in the folder format of Fabric Git integration (`.platform`, `definition.pbism`, `definition/` with TMDL), trimmed to two tables. The measures are in `definition/tables/Sales.tmdl`. |
| `modeling-guidelines.md` | The team's rules for measures, M1 to M6. |
| `review/colleague-review.md` | Jonas's review: five numbered statements and a verdict. |
| `.claude/agents/reviewer.md` | A reviewer subagent that can only read (`tools: Read, Grep, Glob`). |
| `CLAUDE.md` | Two lines on how the team cites rules and TMDL. |

`.claude/` is a hidden folder: `ls -a` shows it.

## Steps

### 1. Look around (3 min)

In the second terminal:

```
cd /var/tmp/03-reviewer
cat review/colleague-review.md
cat modeling-guidelines.md
cat .claude/agents/reviewer.md
```

Read the reviewer's definition: which tools does it get, and what does its body tell it to assume?

### 2. Mark each statement, spot-check two (6 min)

In `sign-off.md`, table "Step 2", mark each of Jonas's five statements:

- `G` (grounded): it cites a place you can look up, a file and line or a rule ID.
- `U` (ungrounded): it cites nothing in the files.

Grounded doesn't mean correct. It means you can check it. Pick the two grounded statements that would change the model if someone acted on them (they ask for a fix), open the cited lines in `Sales.SemanticModel/definition/tables/Sales.tmdl` and the cited rule in `modeling-guidelines.md`, and read the rule **to the end**. Write `yes` or `no` in "Holds?" for those two.

### 3. Write your first judgment (2 min)

Under "Step 3", one sentence on which statement is the problem and why, in the form "Statement N is wrong, because …", or "Nothing is wrong." if that's what you think. End it with a full stop. Don't change this sentence later; comparing it with the end is part of the exercise.

### 4. Session A: a reviewer after a conversation (6 min)

Start Claude Code in the project folder (`cd /var/tmp/03-reviewer`, then `claude`). On the first start in a folder, Claude Code asks whether you trust it; the preselected answer is "No, exit", so move down to "Yes, I trust this folder". Use the largest model you have (`/model`). Tell Claude what you think, with your sentence from step 3:

```
Read review/colleague-review.md. My first judgment: <your sentence from step 3> Do you agree? Answer in two sentences.
```

Then call the reviewer. Type the mention in full, don't pick a file from the suggestion list:

```
@agent-reviewer Check review/colleague-review.md against modeling-guidelines.md and the TMDL files. Change no file.
```

A line `reviewer(…)` appears; the reviewer runs in the background and Claude reports when it's finished. Press `Ctrl+O` to open the transcript viewer and scroll up with ↑ to the `reviewer(…)` line: below it you see `Prompt:`, the task prompt Claude wrote for the reviewer. Your mention picked the reviewer, but Claude wrote what it got. `Ctrl+O` again closes the viewer.

Under "Step 4", note what that prompt contained besides the files and the job: a hint at a statement, a rule, an exception, your opinion? Also note how Claude introduced the reviewer's result: as a result, or as a confirmation of you?

### 5. Session B: the same call, fresh (4 min)

Type `/exit`, start `claude` again, and send only the reviewer prompt from step 4, nothing before it. `Ctrl+O` again. Under "Step 5", note the same things. What's different?

The reviewer starts with its own fresh context in both sessions. It never sees your conversation. It sees what Claude writes into its task prompt, and in session A Claude had already read the files and discussed them with you. Whether any of that shows up in the prompt varies from run to run; only `Ctrl+O` tells you.

### 6. Check one finding at the source (4 min)

Take one finding from the reviewer in session B that would change the release: a statement it says doesn't hold. Open the file and line it names, and the rule. Under "Step 6", write the statement number, what the reviewer said, and a quote from the source that settles it, copied word for word, in quotation marks or on a line starting with `>` (Markdown backticks may stay or go).

The reviewer's report is the output of a model, like Jonas's review. It may also list things that are matters of taste ("is `LY` readable enough?"). They are not rule violations unless a rule says so.

### 7. Decide (3 min)

Under "Step 7", write the final decision for each statement: `keep`, `strike` or `not a fact`. Then, in the second terminal, from `03-reviewer/`:

```
python3 check.py --project /var/tmp/03-reviewer --notes /var/tmp/03-notes
```

### 8. Optional: your own semantic model (10 min)

Only if you have a semantic model in a Fabric workspace connected to Git, or saved as a Power BI project (PBIP) in TMDL format, and a few written team rules. Copy its `definition/` folder and your rules into a fresh folder outside any repository, copy `.claude/agents/reviewer.md` next to them, and run step 5 against it: a fresh session, only the reviewer prompt, `Ctrl+O`, then check one finding at the source. There's no expected result for this step; the question is whether a finding survives your look at the source.

## What a good result looks like

- **Step 2:** statements 1 to 4 are `G`, statement 5 is `U` ("common DAX best practices" and "will perform well" cite nothing). Your two spot checks include statement 2, and it doesn't hold: M1 says "When the denominator is a constant, such as `/ 12`, use the `/` operator.", and `Sales.tmdl:22` is `[Total Sales] / 12`.
- **Step 3:** one sentence, written before any reviewer ran. It's fine if it was wrong; it shows what you would have released.
- **Step 4:** the task prompt names the files and the job. In the tests for this exercise it carried more from the conversation in three of eleven runs, for example "including any exceptions written into the rule" (all three on an earlier version of Claude Code). In all eleven, Claude tied the result to your judgment, for example "The reviewer agrees with your judgment". If your prompt carried nothing extra, note that: it's the most common outcome.
- **Step 5:** the task prompt names files, job and format, and Claude presents the result on its own terms. Your note says why that matters: the reviewer's context is fresh in both sessions, but only session B starts from nothing you and Claude had already decided, and only the task prompt shows the difference, not the result.
- **Step 6:** a quote that is literally in `modeling-guidelines.md` or `Sales.tmdl`.
- **Step 7:** keep 1, 3 and 4; strike 2; statement 5 is not a fact. Jonas's verdict becomes "ready to release after the fix for statement 4".
- **Project:** no file changed, and the reviewer's `tools` line still lists only reading tools.
- **`check.py`:** prints "all checks passed".

## Why it works this way

- A subagent starts with a fresh, isolated context window. It doesn't see your conversation history; Claude composes a delegation message that summarizes the task (code.claude.com/docs/en/sub-agents, "What loads at startup"). The project's `CLAUDE.md` loads for it too.
- An @-mention guarantees which subagent runs, not what it receives: "Your full message still goes to Claude, which writes the subagent's task prompt based on what you asked." (sub-agents, "Invoke subagents explicitly")
- A subagent with only `tools: Read, Grep, Glob` can't edit anything, and that limit is enforced by Claude Code rather than requested in a prompt (code.claude.com/docs/en/best-practices). Without a `tools` field it inherits every tool.
- A reviewer that's asked to find problems will always find something (best-practices, "Review against your spec"). Its findings are a starting point for your decision, not the decision.
- A fork is a subagent that inherits the whole conversation and isn't independent; fork mode is on by default in interactive sessions (sub-agents, "Fork the current conversation"). The @-mention makes sure your reviewer runs instead.
- In DAX, `DIVIDE()` is recommended when a denominator could be zero or blank, and the `/` operator when the denominator is a constant (learn.microsoft.com/dax/best-practices/dax-divide-function-operator). Rule M1 follows that guidance.
