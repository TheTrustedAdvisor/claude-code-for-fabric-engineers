# Exercise 6: What does /rewind undo, and what needs Git?

Companion exercise to video 6, "Undo in Claude Code: /rewind, Git and what neither covers". About 30 minutes. Everything runs locally; no Fabric capacity needed. Only the optional step 8 uses a real workspace.

## Scenario

- **Role:** You're a data engineer on a team that keeps a Fabric project in Git.
- **Situation:** The project has a notebook in Git format (`daily_counts.Notebook/`) and a script that cleans the raw counts (`clean_counts.py`). The repository has one commit, "baseline". Claude is about to make three changes you'll want to take back.
- **Task:** Let Claude change three things with three different tools, predict what `/rewind` brings back, check it with Git, and undo the rest yourself until `git status` shows only your own note.
- **Tools:** `/rewind` (or `Esc` twice), `git status`, `git diff`, `git restore`, `git clean`, a second terminal.

## Before you start

- Claude Code installed and signed in. Git and Python 3 as `python3`: check with `git --version` and `python3 --version`.
  - **macOS, Linux, WSL:** use your normal terminal.
  - **Windows:** install Git for Windows. Start Claude Code from PowerShell or Windows Terminal and use Git Bash for every other command in this exercise. The project turns off Claude Code's PowerShell tool (`CLAUDE_CODE_USE_POWERSHELL_TOOL=0` in `.claude/settings.json`), so `cp` and `sed` run in Git Bash. Started from inside Git Bash, Claude Code may not find Git Bash; then first point it to Git Bash: `export CLAUDE_CODE_GIT_BASH_PATH='C:\Program Files\Git\bin\bash.exe'` for the default installation, or the `bin\bash.exe` of your Git installation (a per-user installation is under `%LOCALAPPDATA%\Programs\Git`).
- Open a second terminal. Run Git commands and checks there, not with `!` inside Claude Code.
- Create the project outside your own projects and outside any folder that has a `CLAUDE.md` above it: Claude Code also loads `CLAUDE.md` files from every folder above the one you start in. The examples use `/var/tmp`; in Git Bash on Windows use a folder in your user profile, for example `~/work/06-undo`. The setup script refuses a folder inside a Git repository or below a `CLAUDE.md`. Your personal `~/.claude/CLAUDE.md` still loads; that's fine for this exercise.
- Close the project's files in your editor between steps. An editor that keeps a file open may save its own copy again later and hide what `/rewind` did.

In the second terminal, from this folder (`06-undo/` in the companion repo):

```
./setup.sh /var/tmp/06-undo
```

It creates a Git repository on `main` with one commit, "baseline", and your note `notes.md`, which stays untracked. In PowerShell instead of Git Bash, `python3 setup.py /var/tmp/06-undo` does the same. To start over, delete the folder and run setup again.

## What's in the project

| Path | What it is |
|---|---|
| `daily_counts.Notebook/` | A Fabric notebook in Git format: `.platform` and `notebook-content.py`, the way Fabric Git integration stores it. |
| `clean_counts.py` | A local script that cleans the raw counts. In this exercise it's only changed, never run. |
| `.claude/settings.json` | Turns off the PowerShell tool, so shell commands run in Bash (Git Bash on Windows). No permission mode: the session starts in your own default, auto mode in current versions. |
| `notes.md` | Your note, with three headings. Not in Git. |

## Steps

### 1. Look around (2 min)

In the second terminal:

```
cd /var/tmp/06-undo
git status
git log --oneline
```

`git status` lists `notes.md` under "Untracked files", nothing else. `git log` shows one commit, "baseline".

### 2. Three changes, three tools (5 min)

Start Claude Code in the project folder (`claude`). Claude Code asks whether you trust the folder; the preselected answer is "No, exit". Choose "Yes, I trust this folder". Then type this prompt:

```
Make a backup copy clean_counts.bak.py of clean_counts.py with cp in the shell. Then change the heading in the markdown cell of daily_counts.Notebook/notebook-content.py to "Daily bike counts, Zurich", with your Edit tool. Rename the columns bikes_in and bikes_out to count_in and count_out in clean_counts.py, with sed in the shell. Nothing else.
```

In auto mode (the status line shows "auto mode on"), the three changes run without a prompt. Read the tool calls in the transcript: `Bash(…)` for a shell command, `Update(…)` for a change with the Edit tool. Claude may also read files first (shown as "Read 1 file"). In manual mode, Claude Code asks first: read each prompt before you answer "1. Yes". Its first line says the kind, "Bash command" or "Edit file"; afterward the transcript only says "Ran 1 shell command" for the shell calls. Either way, note which change came with which kind; expect at least one of each. If auto mode blocks `cp` or `sed`, approve it under `/permissions` → Recently blocked and ask Claude to retry, or start over with a fresh folder. Stop Claude (`Esc`) if it starts a search outside the project folder (for example `find /`).

After each answer, Claude Code may show a grayed-out suggestion in the input, such as "commit these changes". Never send it with Enter; type your next prompt over it. A commit would change what this exercise checks.

If something goes differently:

- **Claude says it can't find the notebook, or uses its Edit tool for `clean_counts.py` instead of `sed`:** the exercise loses its point. Exit Claude Code, delete the folder, run setup again and send the prompt once more.
- **`git status --short` doesn't list ` M clean_counts.py`:** on macOS, `sed` may have changed nothing (it needs `sed -i ''`, and it doesn't know `\b`). Make the change yourself in the second terminal: `sed -i.orig 's/bikes_in/count_in/; s/bikes_out/count_out/' clean_counts.py && rm clean_counts.py.orig`.

In the second terminal:

```
git status --short
```

### 3. Your own line, and a prediction (3 min)

Open `daily_counts.Notebook/notebook-content.py` in your editor. At the end of the line under the heading (`# One row per counting station and day, for the city's traffic report.`) add a sentence of your own, for example ` Reviewed by Ana, Nov 5.` Save and close the editor.

Then, before you open `/rewind`, write your prediction under "Prediction" in `notes.md`: after "Restore code", which of the three files are back as in the baseline, and does your own line stay?

### 4. Rewind (3 min)

In Claude Code, type `/rewind` (or press `Esc` twice with an empty input). The list shows your prompts and, under each one, the files it would restore (or "No code changes"). The cursor starts on "(current)"; move up with the arrow key to the prompt from step 2 and press Enter.

Read the confirmation before you choose: which file does it restore, with how many lines, and what does the line with ⚠ at the bottom say? Then choose "3. Restore code" (it keeps the conversation).

In the second terminal:

```
git status --short
```

Is your own line still in the notebook file? Compare with your prediction.

### 5. Ask Claude (2 min)

In Claude Code:

```
Run git status and tell me which of your three changes are still there, and why.
```

In manual mode, answer "1. Yes" if Claude asks to run `git` commands. Read the answer. Does Claude know that you rewound? Compare its reason with what you did. Whatever it says, `git status` in your own terminal is the record.

### 6. The rest with Git (5 min)

In the second terminal, see what's still changed and take it back:

```
git diff
git restore clean_counts.py
git status --short
```

The backup copy is still there, under `??`: Git never had it, so `git restore` can't help. Ask Git first what a clean would delete:

```
git clean -n
```

It lists the backup copy and your `notes.md`. `git clean -f` without a file name would delete both. So delete only the one:

```
git clean -f clean_counts.bak.py
git status --short
```

Now `git status --short` shows only `?? notes.md`.

If you staged a file with `git add` along the way, `git diff` shows nothing and `git restore <file>` does nothing; then use `git restore --staged --worktree <file>`. A staged backup copy isn't removed by `git clean`; run `git rm --cached clean_counts.bak.py` first. With Git older than 2.23, `git checkout -- <file>` does what `git restore <file>` does.

### 7. Write it down (3 min)

In `notes.md`:

- **What happened:** for each of the three files (the notebook, `clean_counts.py`, the backup copy), what brought it back: the checkpoint or Git, and which command. And what happened to your own line, and why.
- **My rule for undoing Claude's changes:** when you use `/rewind`, when Git, what you check afterward, and what you do before Claude starts a bigger change.

### 8. Optional: the workspace stays (10 min)

Only if you have a Fabric workspace you may change (dev or sandbox, never production) and the `fab` command line, signed in. Setup in [`fabric/README.md`](fabric/README.md).

In the second terminal, back in `06-undo/` of the companion repo:

```
./setup.sh /var/tmp/06-undo-fabric --fabric
cd /var/tmp/06-undo-fabric
export FABRIC_DEV_WORKSPACE='<name of your dev workspace>'
./deploy.sh dev
./show.sh
```

`show.sh` reads the notebook back from the workspace and prints its heading: "Bike counts per day". Start Claude Code in this folder (trust it; the settings allow `./deploy.sh dev`) and send two prompts, one after the other:

```
Change the heading in the markdown cell of daily_counts.Notebook/notebook-content.py to "Daily bike counts, Zurich", with your Edit tool. Nothing else.
```

```
Now deploy the notebook to dev.
```

Two prompts, so the deploy can only start after the edit is done. Run `./show.sh`: the workspace now says "Daily bike counts, Zurich". Then `/rewind`: under the deploy prompt the list says "No code changes". Select the first prompt and choose "3. Restore code". In the second terminal:

```
git status --short
./show.sh
```

The repository is back at the baseline; the workspace still says "Daily bike counts, Zurich". Neither `/rewind` nor `git restore` reaches it. If your workspace is connected to Git and the baseline notebook was committed from it before you started Claude (**Source control** → **Changes** → **Commit**), its list now shows the notebook as "Uncommitted". Then **Source control** → **Changes** → select the notebook → **Undo**, and confirm with **Undo**: it goes back to the commit the workspace is synced to. Without that first commit the notebook counts as a new item, and Undo deletes it. Without a Git connection, bring it back from Git through the same deploy:

```
./deploy.sh dev
./show.sh
```

Add one sentence to `notes.md` in the first project (`/var/tmp/06-undo`): what brought the workspace back?

### 9. Check yourself (2 min)

In the second terminal, from `06-undo/`:

```
python3 check.py --project /var/tmp/06-undo
```

It checks the end state: the history (one commit, "baseline"), the files (as in the baseline), `git status` (only `?? notes.md`) and that the backup copy is gone. For your note it only checks that the sections are filled and name the files, your own line, `/rewind` and Git; whether what you wrote is right, you judge yourself against "What a good result looks like". Each failed check says why in one line.

## What a good result looks like

- **Step 2:** in auto mode, `Bash(…)` calls for `cp` and `sed` and one `Update(…)` for the notebook, no prompt; in manual mode, "Bash command" prompts for `cp` and `sed` and one "Edit file" prompt for the notebook. `git status --short` shows ` M clean_counts.py`, ` M daily_counts.Notebook/notebook-content.py`, `?? clean_counts.bak.py`, `?? notes.md`.
- **Step 4:** the list shows `notebook-content.py +2 -2` under your prompt (Claude's heading and your line); `clean_counts.py` isn't listed. The confirmation says "The code will be restored +2 -2 in notebook-content.py." and warns: "Restored files go back whole, losing later changes by anyone. Bash changes to other files are not undone." After "Restore code", the notebook is back at the baseline, and your own line is gone with it. `clean_counts.py` (changed by `sed`) and `clean_counts.bak.py` (made by `cp`) stay.
- **Step 5:** Claude may not know that you rewound. In our local runs it said that something outside the session had changed the notebook back. Your own `git status` is what counts.
- **Step 6:** `git restore clean_counts.py` brings the script back, `git clean -n` lists the backup and `notes.md`, `git clean -f clean_counts.bak.py` deletes only the backup. In the end `git status --short` shows only `?? notes.md`.
- **Step 7:** your rule, for example: "I undo Claude's file edits with /rewind and shell changes with Git, and run git status afterward, because a checkpoint covers only the files Claude edited with its file tools. I don't add my own lines to a file Claude just changed until I've committed or rewound its change, and once it's committed, I undo with Git. I commit before a bigger change."
- **Step 8 (optional):** after the deploy prompt, the rewind list says "No code changes". After "Restore code" on the first prompt, `git status` is clean, and `show.sh` still prints "Daily bike counts, Zurich". After `./deploy.sh dev` from the restored files, it prints "Bike counts per day" again.
- **`check.py`:** prints "all checks passed".

## Why it works this way

- Every prompt that starts a turn creates a checkpoint, and before Claude edits a file with its file tools, Claude Code snapshots it (code.claude.com/docs/en/checkpointing, "How checkpoints work"; code.claude.com/docs/en/how-claude-code-works, "Undo changes with checkpoints").
- A file that only Bash commands changed isn't tracked and stays as it is. Once Claude has edited a file with its file tools, `/rewind` also undoes later changes to that file, whatever made them: a shell command, or you (checkpointing, "Bash command changes not tracked", "External changes not tracked"). That's why your own line went too.
- Actions that affect remote systems, such as databases, APIs and deployments, can't be checkpointed (how-claude-code-works). Checkpoints are for quick recovery within a session; for permanent history, use Git (checkpointing, "Not a replacement for version control").
- With Fabric Git integration, a workspace connected to Git can undo changes that aren't committed yet, from its Source control panel; data isn't stored in Git (learn.microsoft.com/fabric/cicd/git-integration/git-get-started, learn.microsoft.com/fabric/cicd/best-practices-cicd).
- `git restore` brings a tracked file back from the last commit; `git clean` deletes files Git doesn't track, and `-n` only shows what it would delete (git-scm.com/docs/git-restore, git-scm.com/docs/git-clean).
