# Exercise 2: Review a semantic model by your team's rules

Companion exercise to video 2, "Reference documents: review a Fabric model by your team's rules". About 30 minutes. Everything runs locally on TMDL files; no Fabric capacity needed. Only the optional step 7 uses a model of your own.

The semantic model and the guidelines are the same as in exercise 3, where a reviewer checks a colleague's review of this model.

## Scenario

- **Role:** You're on a team that keeps its Fabric semantic models in Git, as TMDL files.
- **Situation:** A colleague asks Claude to review the measures of the `Sales` model before it's released. Claude finds a lot. Your team has written guidelines for its measures, and by those guidelines, most of the list isn't a problem at all.
- **Task:** Run the review without and with the team's guidelines in the context, predict what changes, change one rule, and see what that does to the result.
- **Tools:** `@` file references, `/context`, `/clear`, a second terminal.

## Before you start

- Claude Code installed and signed in. Python 3 as `python3` (check with `python3 --version`) for the setup and the check. Git is optional.
  - **macOS, Linux, WSL:** use your normal terminal.
  - **Windows:** run the setup and the check in Git Bash, or use `python setup.py …` and `python check.py …` in PowerShell. Claude Code can run in either.
- Open a second terminal for the setup, your editor and the check.
- Create the project outside your own projects and outside any folder that has a `CLAUDE.md` above it: Claude Code also loads `CLAUDE.md` files from the folders above the one you start in, and they would change the review. The examples use `/var/tmp`; on Windows use a folder in your user profile, for example `~/work/02-reference`. The setup script refuses a folder inside a Git repository or below a `CLAUDE.md`.
- Keep your notes outside the project, for example in `/var/tmp/02-notes`, so Claude doesn't read your predictions.

In the second terminal, from this folder (`02-reference/` in the companion repo):

```
./setup.sh /var/tmp/02-reference --notes /var/tmp/02-notes
```

**Permission mode:** the project sets no mode, so Claude Code starts in its default, auto mode (Claude Code v2.1.283 or later; the status line shows "⏵⏵ auto mode on"). Reading files and writing into the project run without asking; other actions go to a classifier instead of a permission prompt. In this exercise Claude only reads the model and writes into `reviews/`, which the setup creates empty, though it may also look something up on the web. If your organization turned auto mode off, Claude Code starts in manual mode and asks before it writes a file and before most commands: then read each permission prompt and choose "1. Yes", not "don't ask again".

**First start in the project folder:** Claude Code asks whether you trust the folder. The preselected answer is "No, exit"; choose "Yes, I trust this folder".

## What's in the project

| Path | What it is |
|---|---|
| `Sales.SemanticModel/` | A semantic model as a Power BI project (PBIP) saves it, and as Fabric Git integration stores it: `definition.pbism`, `.platform` and a `definition/` folder with one TMDL file per table. |
| `Sales.SemanticModel/definition/tables/Sales.tmdl` | Six measures, each with a description (`///`), and four columns. Direct Lake on a lakehouse. |
| `Sales.SemanticModel/definition/tables/Date.tmdl` | The date table. |
| `.claude/settings.json` | Project settings, empty: no mode set, so auto mode applies. |

The team's guidelines are **not** in the project yet. They're in this folder, at `team/modeling-guidelines.md`; step 4 brings them in. Your notes template is `notes.md` in the notes folder. `check.py` stays here in `02-reference/` (step 8).

## Steps

### 1. Look around (3 min)

In the second terminal:

```
cd /var/tmp/02-reference
ls Sales.SemanticModel/definition/tables
```

Open `Sales.tmdl` in your editor. A `measure` line holds the DAX expression, the `///` line above it is its description, and the indented lines below it are its properties, such as `formatString`.

### 2. Review without the guidelines (5 min)

Start Claude Code in the project folder (`cd /var/tmp/02-reference`, then `claude`) and trust the folder. Choose Opus with `/model` and press `s` to use it for this session only (Enter would make it your default for new sessions); it's the model used in the video, and with another model the lists can differ. Then:

```
Review the semantic model in Sales.SemanticModel. List the problems you find, one line each, with file:line. Write the list to reviews/without.md.
```

When it's done, type `/context` and note the value for "Messages". In `notes.md`, section "Step 2": the number of findings and that value.

### 3. Predict (3 min)

Open `team/modeling-guidelines.md` (in this exercise folder, not in the project) in your editor and read every rule to the end. Then go through `reviews/without.md`: which findings break a rule in the guidelines? Write the file:line of each finding you expect to stay into `notes.md`, section "Step 3". Do this before step 4.

### 4. Review against the guidelines (5 min)

In the second terminal, from this folder:

```
cp team/modeling-guidelines.md /var/tmp/02-reference/
```

Back in Claude Code, type `/clear`, so the first review isn't in the context anymore, then:

```
Review the semantic model in Sales.SemanticModel against @modeling-guidelines.md. List the problems you find, one line each, with file:line. Write the list to reviews/with.md.
```

`@modeling-guidelines.md` puts the file into your message, so the guidelines are in the context before Claude starts. You see it as a line `Read modeling-guidelines.md`. Then `/context` again. In `notes.md`, section "Step 4": the number of findings, the Messages value, and which of your predictions held.

### 5. Change one line, change one finding (8 min)

In the second terminal:

```
cd /var/tmp/02-reference
cp modeling-guidelines.md modeling-guidelines-b.md
```

Pick one rule in `modeling-guidelines-b.md` and decide how to change its text so that **exactly one** finding of step 4 changes: one drops, or one new one appears, and nothing else. Before you edit, write the rule ID and the finding you expect to change into `notes.md`, section "Step 5". Then change only the text of that one line and keep its ID. Leave `modeling-guidelines.md` as it is.

In Claude Code: `/clear`, then

```
Review the semantic model in Sales.SemanticModel against @modeling-guidelines-b.md. List the problems you find, one line each, with file:line. Write the list to reviews/with-b.md.
```

Did exactly that finding change? If more changed, read your new line the way Claude does: as written. Reword it, `/clear`, and run the prompt again. Note what happened under "Step 5".

### 6. One task per session (2 min)

Tomorrow you have three semantic models to review against the same guidelines. In `notes.md`, section "Step 6": one sentence on whether you'd review them in one session or in three, and why. Your two `/context` values from steps 2 and 4 help.

### 7. Optional: a model of your own (10 min)

Only with a semantic model you're allowed to share with Claude. Get its TMDL files in one of two ways:

- **Power BI Desktop:** save the file as a Power BI project (`.pbip`); for a Direct Lake model you're live editing, File > Export > Power BI Project (PBIP). The `.SemanticModel` folder next to the `.pbip` file is what you need. It must hold a `definition/` folder with `.tmdl` files; a `model.bim` file instead means the project was saved in the older TMSL format (learn.microsoft.com/power-bi/developer/projects/projects-dataset, "TMDL format").
- **Fabric Git integration:** if the workspace is connected to Git, the model is already in the repository in the same format.

Copy the `.SemanticModel` folder into a new folder outside your projects, together with your team's guidelines (or the ones from this exercise), and run the prompt from step 4 with the folder name of your model. A TMDL file holds metadata, not data, but expressions name servers and databases: follow your company's rules for what you may share. `check.py` doesn't check this step.

### 8. Check yourself (2 min)

In the second terminal, from `02-reference/`:

```
python3 check.py --project /var/tmp/02-reference --notes /var/tmp/02-notes
```

It checks `reviews/without.md` (five or more distinct places cited with file:line), `modeling-guidelines.md` (in the project, unchanged), `reviews/with.md` (the expected violation, nothing else), `modeling-guidelines-b.md` (exactly one rule line changed), `reviews/with-b.md` (exactly one finding changed compared with step 4, under the rule you changed) and `notes.md` (filled in). Each failed check says why in one line.

## What a good result looks like

- **Step 2:** a long list, in the tests 8 to 11 findings in four auto-mode runs (8 to 13 across eight runs, with the four in manual mode): `Margin %` has no format string, `Avg Monthly Sales` divides by a fixed 12, no month column, visible `Amount` and `Cost` columns, a hard-coded data source, and more. Some of it is useful; it isn't what your team decided.
- **Step 4:** exactly one finding: **M2** for `'Margin %'` at `Sales.tmdl:17` (no `formatString`). The `/ 12` in `Avg Monthly Sales` is not a finding: M1 says to use `/` when the denominator is a constant. Claude often adds which rules hold. The findings follow the guidelines, not Claude's taste.
- **Step 4, `/context`:** "Messages" after each review between 8k and 15k tokens in the tests: the TMDL files are most of it, the guidelines are small. Right after `/clear` it starts near zero again.
- **Step 5:** exactly one finding changed. A change that works, for example: delete the last sentence of M1, so it reads "Divide with `DIVIDE()`, so a zero or blank denominator returns blank instead of an error." Then `Avg Monthly Sales` at `Sales.tmdl:22` is a new M1 finding, and Claude says why: the rule, as written, has no exception any more.
- **Step 6:** three sessions, with `/clear` in between: each review needs only its model and the guidelines, and the earlier models would stay in the context, cost tokens on every turn, and add nothing.
- **`check.py`:** prints "all checks passed".

## Why it works this way

- Claude answers from what's in its context: the conversation, the files it read and its instructions (code.claude.com/docs/en/how-claude-code-works, "The context window"). Your team's rules are in the context only if someone puts them there.
- `@` includes the content of a file in your message, as long as it fits the Read tool's token limit (code.claude.com/docs/en/common-workflows, "Reference files and directories").
- `/clear` starts a new conversation with an empty context; run it when you switch to unrelated work, because old conversation crowds out the files you need next and costs tokens on every message (code.claude.com/docs/en/context-window, "When your context fills up"). A focused context gets better answers and costs less (code.claude.com/docs/en/best-practices, "What you can stop doing").
- A rule that should apply in every session belongs in `CLAUDE.md`, which can also import a file such as your guidelines with `@path` (code.claude.com/docs/en/memory, "Import additional files"). Video 5 is about CLAUDE.md.
- A Power BI project saves a semantic model in TMDL with one file per table (learn.microsoft.com/power-bi/developer/projects/projects-dataset), and Fabric Git integration stores semantic models in the same format (learn.microsoft.com/fabric/cicd/git-integration/source-code-format).
- M1 follows Microsoft's guidance: DIVIDE when the denominator can be zero or blank, the `/` operator when it's a constant (learn.microsoft.com/dax/best-practices/dax-divide-function-operator).
