# Exercise 4: What runs besides the model?

Companion exercise to video 4, "Claude Code harness: what runs besides the model?". About 30 minutes. Everything runs locally; no Fabric capacity needed. Only the optional step 8 talks to Fabric.

## Scenario

- **Role:** You're a data engineer on a team that keeps a Fabric project in Git.
- **Situation:** The project has a notebook and two `CLAUDE.md` files: one in the project root with the team's rules, and one in `notebooks/` with a rule only for notebooks. Claude doesn't seem to know that second rule, although it's right there in the folder.
- **Task:** See what's loaded before your first prompt, watch when the notebook rule comes into the context, make it load from the start, and name every part besides the model: where it comes from and where you see it.
- **Tools:** `/context all`, `/memory`, `/permissions`, `/hooks`, `/clear`, an `@path` import, a second terminal.

## Before you start

- Claude Code installed and signed in. Python 3 as `python3`: check with `python3 --version`.
  - **macOS, Linux, WSL:** use your normal terminal.
  - **Windows:** start Claude Code from PowerShell or Windows Terminal, and use Git Bash for every other command in this exercise. In PowerShell, `python3 setup.py …` does the same as `./setup.sh …`.
- Open a second terminal. Run scripts and checks there, not with `!` inside Claude Code.
- Create the project outside your own projects and outside any folder that has a `CLAUDE.md` above it: Claude Code also loads `CLAUDE.md` files from every folder above the one you start in. The examples use `/var/tmp`; on Windows use a folder in your user profile, for example `~/work/04-harness`. The setup script refuses a folder inside a Git repository or below a `CLAUDE.md`.
- If you have your own `~/.claude/CLAUDE.md`, plugins or MCP servers, they load too, and your numbers in `/context all` will differ from the ones below. That's part of the lesson: your profile is part of the harness.

In the second terminal, from this folder (`04-harness/` in the companion repo):

```
./setup.sh /var/tmp/04-harness --notes /var/tmp/04-notes
```

**Permission mode:** the project sets manual mode (`"defaultMode": "default"`), so Claude Code asks before any command that isn't on its built-in read-only list and that no rule allows. It also turns off auto memory for this project, so notes from an earlier run can't change what Claude knows.

**First start in the project folder:** Claude Code shows a trust dialog. The preselected answer is "No, exit". Choose "Yes, I trust this folder".

## What's in the project

| Path | What it is |
|---|---|
| `CLAUDE.md` | The team's rules for the whole project. |
| `notebooks/CLAUDE.md` | One rule that only matters for notebooks. |
| `notebooks/load_orders.Notebook/` | A Fabric notebook in Git format. |
| `.claude/agents/reviewer.md` | A subagent definition: a reviewer that may only read. |
| `.claude/settings.json` | Manual mode, auto memory off, and one deny rule. On Windows it also turns off Claude Code's PowerShell tool, so every shell command goes through the Bash tool the rule is written for. |

`.claude/` is a hidden folder: `ls -a` shows it, and in a file manager turn on hidden files (macOS Finder: Cmd+Shift+.).

In the notes folder: `harness.md`, with two tables and two short questions. `check.py` stays here in `04-harness/` (step 9).

## Steps

### 1. Look around (3 min)

In the second terminal:

```
cd /var/tmp/04-harness
cat CLAUDE.md
cat notebooks/CLAUDE.md
cat .claude/settings.json
```

### 2. Before the first prompt (3 min)

Start Claude Code in the project folder (`cd /var/tmp/04-harness`, then `claude`) and trust the folder. Before you type anything:

```
/context all
```

Look at the lines under "Estimated usage by category" and the lists below them. Which `CLAUDE.md` is listed under "Memory files"? Is `notebooks/CLAUDE.md` there? Which agent is listed under "Custom agents"? If the output is longer than your window, scroll up. Esc closes it. In `harness.md`, first table, row "before the first prompt".

### 3. Ask what Claude knows (2 min)

```
Which rules do you know right now for working with the notebooks? Don't read any file, answer only from what you already know.
```

Does Claude name a rule about time zones? Row "after step 3".

### 4. Let Claude read a notebook (5 min)

```
Use your Read tool to read notebooks/load_orders.Notebook/notebook-content.py. When did the last load run?
```

Look at the lines right below "Read 1 file". What's there? In which time zone does Claude give the timestamp in the notebook? Then send the question from step 3 again, and run `/context all` once more. Row "after reading the notebook".

Now type `/clear` and send the question from step 3 a third time. Row "after /clear".

Under the table, write one sentence: what brought the rule into the context, and which line showed it? If you saw no `Loaded` line, press Ctrl+O for the detailed view (Ctrl+O again to go back): the line can sit there. Reading the file with the Read tool or with a single-file shell read such as `cat` or `head` both load the rule (code.claude.com/docs/en/memory).

### 5. Load the rule from the start (4 min)

Make the rule from `notebooks/CLAUDE.md` apply before Claude reads any notebook. In your own editor, add this line at the end of the project's `CLAUDE.md` (an import):

```
@notebooks/CLAUDE.md
```

On Windows too, write `/`, not `\`. Save, type `/exit` in Claude Code, start `claude` again, and run `/context all`. What's under "Memory files" now? Ask the question from step 3 once more. Row "after the import".

### 6. Name the parts (6 min)

Look at each part, then fill in the second table in `harness.md`: where it comes from (Claude Code, the project, your profile, you) and where you saw it.

- `/context all`: System prompt, System tools, Custom agents, Memory files. You see the size of the system prompt and the tools, not their text.
- `/memory`: which instruction files Claude Code knows about. Esc closes it.
- `/permissions`: switch tabs with the arrow keys. What's on the "Deny" tab? To see where a rule comes from, select it with ↓ and press Enter: the dialog asks whether to delete it and names its source ("shared project settings" is `.claude/settings.json`). Keep "No" and press Esc twice.
- `/hooks`: are there any? Esc closes it.
- The agent definition: open `.claude/agents/reviewer.md` in your editor, or `cat` it in the second terminal.

Then fill in the last section of `harness.md`: one sentence on what you check before the first prompt, which command you use, and why.

### 7. A Fabric tool is just a tool (3 min)

```
List my Fabric workspaces with the fab command line.
```

Claude writes a shell command, and Claude Code asks you. Read the prompt: which tool is it, and which command? Answer "4. No". (The transcript may still say "Ran 1 shell command" above "Interrupted": that counts the attempt; `fab` didn't run.) Not "Yes, and don't ask again": that saves an allow rule in `.claude/settings.local.json`. Whether you have the Fabric CLI installed doesn't matter here; you only need the prompt. This prompt is the row "Approval".

Then, in the same session:

```
Run fab rm orders-dev.Workspace/load_orders.Notebook -f now.
```

The workspace doesn't need to exist. If Claude first proposes another command, such as `fab exists …` to check the path, answer "4. No" and send `Don't check first. Run fab rm orders-dev.Workspace/load_orders.Notebook -f now.` Does Claude Code ask you this time? Find Claude Code's own line about the call. Which rule decided, and where did you see it in step 6?

### 8. Optional: the same tool with a real workspace (5 min)

Only if you have the Fabric command line (`pip install ms-fabric-cli`), are signed in with `fab auth login`, and may list the workspaces of that account. `/clear`, send the prompt from step 7 again and answer "1. Yes" this time. In the second terminal, `fab auth status` shows which account `fab` used. Every command Claude runs signs in as that account, with all its rights. Video 5 shows what that means for a deploy to prod. In `harness.md`, last section, add a second sentence below the one from step 6: what you'd check before you let Claude run `fab`.

### 9. Check yourself (2 min)

In the second terminal, from `04-harness/`:

```
python3 check.py --project /var/tmp/04-harness --notes /var/tmp/04-notes
```

It checks `CLAUDE.md` (the team rules are still there, and it imports `notebooks/CLAUDE.md`), `.claude/settings.json` (the deny rule is still there, no allow rule for `fab`), and `harness.md` (the first table compared with the expected result, the second table checked for the expected source and a matching command or file in each row, and the two sentences). Each failed check says why in one line.

## What a good result looks like

- **First table in `harness.md`:**

  | When | Under "Memory files"? | Claude names the time zone rule? |
  |---|---|---|
  | before the first prompt (step 2) | no | - |
  | after step 3 | no | no |
  | after reading the notebook (step 4) | no | yes |
  | after /clear (step 4) | no | no |
  | after the import (step 5) | yes | yes |

- **Step 4:** right below "Read 1 file" the line `Loaded notebooks/CLAUDE.md`. Claude points out that `LAST_LOAD` is a watermark, not a record of the last run, and gives that timestamp as 1 November 2026, 00:30 Zurich time, with 23:30 UTC on 31 October in parentheses. Under "Memory files" there is still only `CLAUDE.md`: a `CLAUDE.md` in a subfolder loads on demand, not at launch, and isn't listed there while it loads that way. After `/clear` the rule is gone again until Claude touches a file in `notebooks/`.
- **Your sentence** names what loaded the rule (Claude reading a file in `notebooks/`) and the `Loaded` line.
- **Step 5:** `CLAUDE.md` ends with `@notebooks/CLAUDE.md`. "Memory files" lists `CLAUDE.md` and `notebooks/CLAUDE.md`, and Claude names the time zone rule without reading anything.
- **Second table:** every row has both columns. System prompt and tools come from Claude Code, and you see only their size in `/context all`. `CLAUDE.md`, `notebooks/CLAUDE.md`, the agent definition and the deny rule come from the project. MCP tools or skills you see in `/context all` come from Claude Code or your profile, not from the project. Approval comes from you, in the permission prompt.
- **Step 7:** a permission prompt "Bash command" for a `fab` command, answered with No. The `fab rm` call is refused without a prompt: `Permission to use Bash with command fab rm … has been denied.` (the command often has `2>&1` after it; the line starts with `Error:` or sits below `Not run · permission denied`). The deny rule `Bash(fab rm *)` from `.claude/settings.json` decided; you saw it on the Deny tab of `/permissions`, and its dialog says "shared project settings". If Claude suggests allowing the command instead: an allow rule can't make an exception to a deny rule (video 5).
- **Last section:** one sentence with a check and its reason, for example: "Before the first prompt I run `/context all` and look at Memory files, because a rule in a subfolder only counts once it's in the context."
- **`check.py`:** prints "all checks passed".

## Why it works this way

- Claude Code is the layer around the model that provides the tools and manages the context the model sees; that layer is the harness (code.claude.com/docs/en/how-claude-code-works, "The agentic loop").
- `CLAUDE.md` files above the working directory load at launch; files in subdirectories load on demand, once Claude reads, writes or edits a file in that subdirectory. A subdirectory's `CLAUDE.md` doesn't appear under "Memory files"; when it loads, a `Loaded` line appears in the terminal (code.claude.com/docs/en/memory, "How CLAUDE.md files load" and troubleshooting).
- `@path` imports are expanded and loaded into context alongside the `CLAUDE.md` that references them; relative paths resolve from the file that contains the import (code.claude.com/docs/en/memory, "Import additional files").
- `/context all` expands the breakdown by category; `/memory` edits the instruction files; `/permissions` lists allow, ask and deny rules and names the settings file each one comes from (select a rule to see it) (code.claude.com/docs/en/commands, code.claude.com/docs/en/permissions).
- For Claude Code, the Fabric command line is a shell command like any other, so Bash permission rules apply to it. A tool from an MCP server, such as a Fabric MCP server, has its own rule name, `mcp__<server>__<tool>` (code.claude.com/docs/en/permissions, "MCP").
- Whatever Claude runs signs in as the account that command uses; in Fabric, what that account may do depends on its workspace role (learn.microsoft.com/fabric/fundamentals/roles-workspaces).
