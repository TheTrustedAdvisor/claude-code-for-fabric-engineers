# Exercise 7: Will your handoff note carry tomorrow?

Companion exercise to video 7, "Handoff notes: continue tomorrow without today's chat". About 25 minutes. Everything runs locally; no Fabric capacity needed. Only the optional step 8 looks at a real workspace.

## Scenario

- **Role:** You're a data engineer moving the nightly pipeline `pl_sales_nightly` from Azure Data Factory to a Fabric pipeline.
- **Situation:** It's the afternoon of day one. The Fabric pipeline is rebuilt and had its first test run: 4 of 30 table copies failed because the source database rejected their logons. Why, and how many copies may run at the same time, is still open. Tomorrow morning a fresh Claude Code session picks this up, and it won't have today's conversation.
- **Task:** Write a handoff note, test with a fresh session what it knows from the note alone, see a finding from the chat go missing, fix the note until it carries, and continue the next morning from the note.
- **Tools:** `/rename`, `claude -p` in a second terminal, `/exit`, `@` to mention a file, `/resume`.

## Before you start

- Claude Code installed and signed in, Python 3 as `python3`, and Git.
  - **macOS, Linux, WSL:** use your normal terminal.
  - **Windows:** start Claude Code from PowerShell or Windows Terminal and use Git Bash for the other commands, as in exercise 5. In PowerShell, `python3 setup.py …` and `python3 check.py …` do the same as the shell scripts.
- Open a second terminal. You run the cold-start tests there.
- Create the project outside your own projects and outside any folder that has a `CLAUDE.md` above it: Claude Code also loads `CLAUDE.md` files from every folder above the one you start in. The setup script refuses such a folder.

In the second terminal, from this folder (`07-handoff/` in the companion repo):

```
./setup.sh /var/tmp/07-handoff
```

On Windows in Git Bash, use a folder in your user profile instead, for example `~/work/07-handoff`.

## What's in the project

| Path | What it is |
|---|---|
| `migration.md` | The state of the migration on the afternoon of day one: what's done, what failed, the open question, what nobody has read yet. |
| `handoff-note.md` | An empty template with four sections: State, Open question, Next step, Files. |
| `workspace/pl_sales_nightly.DataPipeline/` | The Fabric pipeline in Git format (`pipeline-content.json`). |
| `adf/pl_sales_nightly.json` | The old Data Factory pipeline. Read it, never edit it. |
| `config/source.yaml` | The source system and its limits, owned by the DBA team. |
| `logs/` | The test run log and the gateway log of the first test run. |
| `CLAUDE.md` | The project's rules: cite sources as `file:line`, don't edit `adf/`, times in UTC. |

The project is a Git repository with one commit. `check.py` stays here in `07-handoff/` (step 9).

## Steps

### 1. Look around (2 min)

In the second terminal:

```
cd /var/tmp/07-handoff
cat migration.md
cat handoff-note.md
```

### 2. Name the session (1 min)

In the first terminal, start Claude Code in the project folder (`cd /var/tmp/07-handoff`, then `claude`). The trust dialog starts on "No, exit": press the down arrow to select "Yes, I trust this folder", then Enter. Then:

```
/rename sales-migration
```

The name appears on the prompt bar. Tomorrow you'll find the session by this name.

### 3. Get a draft of the note (3 min)

```
Read only migration.md and the template handoff-note.md, no other file. Fill in handoff-note.md for a colleague who starts fresh tomorrow: state with sources, open question, next step with file, files. At most 20 lines.
```

Name both files in the prompt. If you write "read only migration.md", Claude may refuse to open the template and show you the note in the chat instead. Read the note in the second terminal: `cat handoff-note.md`.

After an answer, Claude Code may suggest a follow-up in the prompt field, such as "commit the handoff note". Don't accept it in this exercise; clear the field before you type your next prompt.

### 4. Cold-start test (3 min)

Leave the session open. In the second terminal, in the project folder:

```
claude -p "Read only handoff-note.md and no other file. What is settled, how many copies may pl_sales_nightly run in parallel at most, and which file do you open first and why? Which statement in the note would you not take over unchecked?"
```

`claude -p` starts a fresh session, prints one answer and exits. That session doesn't have today's conversation. It reads the note and, like every session, loads the project's `CLAUDE.md`. Read the answer as if you were the colleague. Create a new file `cold-start.md` (not in the note, or the fresh session would read your test notes too) and write under `1.` what it says about the number of parallel copies. Write down what the fresh session said, in its words, not what you know from the other session.

Sessions started with `claude -p` don't show up in `/resume` or `claude --continue`, so these tests don't clutter your list.

### 5. A finding only in the chat (3 min)

Back in the session `sales-migration`:

```
Read only config/source.yaml and no other file. How many copies may pl_sales_nightly run in parallel at most?
```

Claude knows the number now. If Claude offers to add the finding to the note, say no or ignore the offer: the point is to see the finding go missing. Repeat the cold-start test from step 4 in the second terminal (arrow up brings the command back). What does the fresh session say about the number now? Write it under `2.` in `cold-start.md`.

### 6. Fix the note and test again (5 min)

Add the finding from step 5 to the note yourself, in your editor: the number, how it comes about, and its source (`config/source.yaml` with the lines). Add the date and the session name at the top. Then make the rest of the note agree with it: the open question and the next step must not still say that `config/source.yaml` hasn't been read. A fresh session distrusts a note that contradicts itself, and it's right to.

Run the cold-start test a third time and write the result under `3.`. Would the colleague now start with the right file? Correct the note until it carries. Under `4.`, write one sentence: what you'll check from now on before you end a session, and why.

If the fresh session names a statement it wouldn't take over unchecked, that's a good sign, not a failure. If it's something `migration.md` already settles, add the reason to the note.

### 7. The next morning (5 min)

End the session with `/exit`. It stays saved. Start Claude Code again in the same folder with `claude`. This is a new session. Then:

```
Read @handoff-note.md and do the next step.
```

Claude reads the note, opens the file the next step names, and should propose a fix for the ForEach. It may ask whether to apply it or which value you want. Answer:

```
Yes, set the batchCount to 8 and add what you found to handoff-note.md.
```

Any value from 1 to 16 is a valid fix; 8 is what the old Data Factory pipeline used. Then type `/resume`: yesterday's session `sales-migration` is in the list. Press Esc; you don't need to go back to it.

### 8. Optional: the same in Fabric (5 min)

> **Optional and not verified in a live workspace.** This step follows the Microsoft Learn pages on the ForEach activity and the Monitoring hub; the field names and the empty batch count were not checked in a real workspace for this exercise. Skip it if the portal looks different.

Only if you have a Fabric workspace with a pipeline that has a ForEach activity. Open the pipeline, select the ForEach, and open the **Settings** tab: **Sequential** and **Batch count**. An empty batch count means the default of 20 parallel iterations, at most 50. Then open the pipeline's run history in the Monitoring hub and find the last run. Ask yourself which of today's findings about this pipeline are only in your head or your chat, and write them into a note.

### 9. Check yourself (2 min)

In the second terminal, from `07-handoff/`:

```
python3 check.py --project /var/tmp/07-handoff
```

It checks `handoff-note.md` (four sections filled in, a date, the session name, the limit with its source, a next step that says where to start and doesn't contradict the finding), `cold-start.md` (four items, no number in tests 1 and 2, the number in test 3), the batch count in `pipeline-content.json`, and that `adf/`, `config/`, `logs/` and `migration.md` are unchanged. Each failed check says why in one line.

## What a good result looks like

- **`cold-start.md`:** tests 1 and 2 give **no** number of parallel copies. The fresh session says the note doesn't contain it, even after Claude named it in the session `sales-migration`. Only test 3 names it. Under `4.` is your rule with its reason, for example: "Before I end a session, I test the note with a fresh session, because a new session only knows what's in files."
- **The number:** at most **16** copies in parallel. The login allows 48 sessions, the trigger splits them equally among 3 pipelines, and each copy holds one session (`config/source.yaml`, the 3 pipelines only in a comment).
- **`handoff-note.md`:** four sections without `…`, a date and the session name, the limit with its source, and a next step that names the file to open (`pipeline-content.json`) or, after step 7, the test run to repeat. It never points to the gateway, which `migration.md` already rules out.
- **Step 7:** the new session starts from the note, finds that the ForEach has no batch count, so Fabric runs up to 20 copies at once, and sets a batch count of 16 or less. `/resume` lists `sales-migration`.
- **`check.py`:** prints "all checks passed".

## Why it works this way

- A session is a saved conversation tied to a project directory. `/exit` and `/clear` don't delete it; `/resume` and `claude --resume <name>` bring it back (code.claude.com/docs/en/sessions).
- Each new session starts with a fresh context window, without the conversation history from previous sessions (code.claude.com/docs/en/how-claude-code-works, "Work with sessions"). What the next session should know has to be in a file it reads: `CLAUDE.md`, which loads in every session, or a note you point it to.
- Claude Code can also keep notes across sessions on its own (auto memory), but Claude decides what's worth saving. In the tests for the video, it saved nothing. Run `/memory` to see what it keeps (code.claude.com/docs/en/memory, "Auto memory").
- Continuing yesterday's session is the other option. It has the whole conversation, detours included, and a long one may already be compacted into a summary, where details from early on can be lost (code.claude.com/docs/en/how-claude-code-works, "When context fills up").
- `claude -p` sessions are left out of the session picker and out of `claude --continue` (code.claude.com/docs/en/sessions).
- In a Fabric pipeline, a ForEach without a batch count runs up to 20 iterations in parallel, at most 50 (learn.microsoft.com/fabric/data-factory/data-factory-limitations, "ForEach parallelism"). Set the batch count to what the source can sustain (learn.microsoft.com/fabric/data-warehouse/migration-sql-server-methods).
