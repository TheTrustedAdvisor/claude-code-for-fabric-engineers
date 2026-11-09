# Exercise 1: Why do two runs give two numbers?

Companion exercise to video 1, "Claude Code prompts: why two runs give two numbers". About 35 minutes. Everything runs locally with real open data; no Fabric capacity needed. Only the optional step 6 uses a Fabric workspace.

## Scenario

- **Role:** You're a data engineer. The city's transport committee wants numbers from the bike counters.
- **Data:** The City of Zurich counts bikes at fixed counters every quarter hour and publishes the counts as open data (CC0, see [`SOURCE.md`](SOURCE.md)). The project holds September 2025 as the city publishes it, column names included: `bikes-2025-09.csv` (about 1.1 MB) and `counters.csv` (the list of counters).
- **Task:** Write a prompt you can judge the result of, see what Claude does with the data, ask an open question twice, find out what Claude decided on its own, and make those decisions yourself until the number comes out the same every time.
- **Tools:** a prompt file and `@`, the tool calls in the transcript, `/clear`, a second terminal.

## Before you start

- Claude Code installed and signed in, Python 3 as `python3` (on Windows, `py` works for the scripts too).
- Open a second terminal. Run the setup, the scripts and the check there, not with `!` inside Claude Code.
- Create the project outside your own projects and outside any folder with a `CLAUDE.md` above it: Claude Code also loads `CLAUDE.md` files from every folder above the one you start in. The examples use `/var/tmp`; on Windows use a folder in your user profile, for example `~/work/01-variance`. The setup script refuses a folder inside a Git repository or below a `CLAUDE.md`.

In the second terminal, from this folder (`01-variance/` in the companion repo):

```
python3 setup.py /var/tmp/01-variance
```

(`./setup.sh /var/tmp/01-variance` does the same.) Each run needs a new folder, so you can always start over.

**Permission mode:** the project sets no mode, so Claude Code starts in its default, auto mode (Claude Code v2.1.283 or later; the status line shows "⏵⏵ auto mode on"). Reading and editing files in the project run without asking; other actions, such as running `python3`, go to a classifier instead of a permission prompt. If your organization turned auto mode off, Claude Code starts in manual mode and asks before it writes a file and before most commands: then read each permission prompt and choose "1. Yes", not "don't ask again".

**First start:** the very first time on a machine, Claude Code shows a theme picker and a short safety notice; press Enter for each. Then, in every new folder, it asks whether you trust the folder. The preselected answer is "No, exit"; choose "Yes, I trust this folder".

## Steps

### 1. Look around (2 min)

In the second terminal:

```
cd /var/tmp/01-variance
head -3 bikes-2025-09.csv
cat counters.csv
```

`FK_STANDORT` is the counter (`id1` in `counters.csv`), `DATUM` the start of the quarter hour, `VELO_IN` and `VELO_OUT` the bikes in each direction, `FUSS_*` pedestrians. An empty field means "not measured".

### 2. A prompt with goal, constraints and audience (8 min)

Create `prompt.md` in the project folder, in any editor that saves plain text. It asks: *How many bikes did the Mythenquai counter count in September 2025, and on which day were there the most?* Your prompt names three things:

- **Goal:** what exists at the end.
- **Constraints:** what Claude may do and must not touch, where the result goes (`results/mythenquai.md`), how long it is.
- **Audience:** who reads it.

Read it as if you didn't know the task: can you tell from the text alone what gets delivered?

Start Claude Code in the project folder (`cd /var/tmp/01-variance`, then `claude`) and send:

```
Run the task in @prompt.md
```

Read the tool calls in the transcript (lines like `Bash(python3 …)`): does Claude read the 1.1 MB file into the conversation, or does it run a script over it? Does Claude's answer name a decision you didn't make?

### 3. The same open question, twice (8 min)

Type `/clear`, then ask, without any further details:

```
Do more or fewer people cycle on weekends than on weekdays, and by what percentage?
```

Note the number. If the answer gives more than one (for example one for all counters and one for Mythenquai), note the one it leads with and what it refers to. Claude may also read your files from step 2 and answer for Mythenquai only: that's one of the decisions it made. Then ask in the same session, because only this session still knows its answer:

```
List every decision you made that my question didn't specify.
```

Type `/clear` and send both prompts again. In `results/two-answers.md`, write down both numbers (they can be the same or different) and two or three decisions, as a list, that came out differently or that you would have made differently.

### 4. Make the decisions yourself (10 min)

Write `prompt-2.md`: the same question, for all bike counters, and below it your decisions, one line each. Take them from Claude's lists. Almost always open: how to handle days with missing data, whether Monday 15 September counts as a weekday (Knabenschiessen: city offices and schools in Zurich are closed), whether the correction factor in `counters.csv` applies, which mean is compared, and how the percentage is computed. At the end, ask for a Python script `weekend.py` that prints the numbers.

Then `/clear` and:

```
Run the task in @prompt-2.md
```

Note the numbers. Now move the script out of the project, so Claude can't see it, in the second terminal:

```
mkdir -p /var/tmp/01-keep
mv /var/tmp/01-variance/weekend.py /var/tmp/01-keep/weekend-1.py
```

Back in Claude Code: `/clear`, and the same prompt again. Claude writes `weekend.py` from scratch. Same numbers? If not, a decision is still open: add a line to `prompt-2.md`, and repeat both runs.

### 5. Write down your rule (2 min)

Write `results/answer.md`: what Claude computed with in step 2, and why that's better than reading the file into the conversation; the two numbers from step 3 and the decision that separated them; the number from step 4 and the line in `prompt-2.md` that fixed it; and your own rule for numbers that have to hold, with the reason.

### 6. Optional: the decisions in a measure (15 min)

Only if you have a Fabric workspace on a capacity that you may change. In the workspace:

1. Create a lakehouse and upload `bikes-2025-09.csv` to its **Files** (Get data, Upload files).
2. Create a notebook, attach the lakehouse, paste [`fabric/load_bike_days.py`](fabric/load_bike_days.py) into a cell and run it. It writes two tables: `bike_days` (one row per counter and day, with the number of quarter hours) and `calendar` (September 2025, with 15 September as a holiday).
3. In the lakehouse's SQL analytics endpoint, choose **New semantic model** with both tables (if Fabric asks which kind of Direct Lake, the probe for the video used Direct Lake on SQL), then **Open data model**: add the relationship `bike_days[date]` to `calendar[date]` (many to one) and the three measures from [`fabric/measures.dax`](fabric/measures.dax).
4. Query the measures twice, for example in the model's DAX query view:

   ```
   EVALUATE ROW("Weekday bikes", [Weekday bikes], "Weekend bikes", [Weekend bikes], "Weekend vs weekday %", [Weekend vs weekday %])
   ```

Is it the number your `weekend.py` printed? If your decisions in `prompt-2.md` differ from the ones in the measures, change the measures to match them.

### 7. Check yourself (2 min)

In the second terminal, from `01-variance/`:

```
python3 check.py --project /var/tmp/01-variance --first /var/tmp/01-keep/weekend-1.py
```

It checks that the data files are unchanged, `results/mythenquai.md` (total and busiest day), `results/two-answers.md` (two numbers, a list of decisions), `prompt-2.md` (decisions one per line, 15 September decided, asks for `weekend.py`), runs both scripts and compares their numbers (the percentage and every number with decimals; labels and layout may differ), and checks `results/answer.md`. Each failed check says why in one line.

## What a good result looks like

- **Step 2:** with the raw counts, Mythenquai counted **61,677** bikes in September 2025; the busiest day was **Saturday, September 20, 2025, with 3,586** bikes. If Claude applied the correction factor (0.98), it's about 60,443; then your prompt left that open. The tool calls show a script running over the CSV, not the file being read into the conversation.
- **Step 3:** the numbers can be the same or different. For all counters together, the first tests for the video gave between 24.5 % and 29.9 % fewer bikes on weekends; in later tests, every run led with 28.3 %, but the tables, ranges and decision lists underneath still differed. Some runs read your files from step 2 and led with Mythenquai instead, where it's about 5 % more on weekends; that's a good result too, because "which counters" is then one of the decisions in Claude's list. Claude's lists name well over ten decisions each. `two-answers.md` is good when it lists decisions that would move the number.
- **Step 4:** `prompt-2.md` decides at least 15 September and the missing days. The two scripts, written independently, print **exactly the same numbers**. With the decisions in [`solution/prompt-2.md`](solution/prompt-2.md), that's a weekday sum of 23,364.0, a weekend sum of 16,753.0 and **−28.3 %**. Other decisions give other numbers; they're right when they come out the same every time and are written in `prompt-2.md`.
- **Step 5:** your rule says where the decisions go and what computes the number, for example: "A number that has to hold is computed by a script, from decisions written in the prompt, because otherwise Claude decides whatever the question leaves open, run by run."
- **Step 6 (optional):** with the measures as they are, the DAX query returns −28.3 both times, the same as the solution's `weekend.py`. `Weekday bikes` is 23,364.0 in both. `Weekend bikes` is 16,753.1 in DAX and 16,753.0 in Python: one counter's weekend mean is 1,076.25, and Python's `round` rounds a half to the even digit while DAX's `ROUND` rounds it away from zero. Rounding is a decision too.
- **`check.py`:** prints "all checks passed".

## Why it works this way

- Claude Code is the layer around the model that provides the tools and manages the context the model sees; the model decides, Claude Code runs the tools (code.claude.com/docs/en/how-claude-code-works, "The agentic loop").
- The model doesn't remember anything between requests; Claude Code re-sends the full context every time (code.claude.com/docs/en/prompt-caching). `/clear` starts fresh with an empty context (code.claude.com/docs/en/sessions).
- A prompt, like `CLAUDE.md`, is a non-deterministic instruction: the model reads it and decides (code.claude.com/docs/en/best-practices, "Deterministic and non-deterministic instructions"). If you care which of two reasonable approaches Claude picks, say so up front (same page, "Write a specific prompt").
- Business-critical calculations belong in the semantic model as reviewed measures, so reports and Copilot use consistent business definitions (learn.microsoft.com/power-bi/create-reports/copilot-evaluate-data).
