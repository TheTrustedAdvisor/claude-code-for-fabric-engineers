# Exercise 4: notes for teachers

Expected results per step, and what varies. The participant's checklist is "What a good result looks like" in `../README.md`; this page adds what you see when you run it yourself. Tested with Claude Code v2.1.318 on Linux. `harness.md` in this folder is a filled-in example that passes `check.py`.

| Step | Fixed result (Claude Code or the files decide) | Varies (the model decides) |
|---|---|---|
| 2 | `/context all`: "Memory files" lists only `CLAUDE.md`, "Custom agents" lists `reviewer` | token counts, depending on profile and session (with or without the MCP block); an "MCP tools" block from the participant's account |
| 3 | no time zone rule | whether Claude also mentions the reviewer agent or the commit attribution line |
| 4 | below "Read 1 file": `Loaded notebooks/CLAUDE.md`; the timestamp in Zurich time first; "Memory files" unchanged; after `/clear` the rule is gone | whether Claude mentions the new rule on its own or only when asked again |
| 5 | "Memory files" lists `CLAUDE.md` and `notebooks/CLAUDE.md`; four rules without reading | wording |
| 6 | Deny tab: `Bash(fab rm *)`; Enter on it opens "Delete denied tool?" with "From shared project settings" (keep "No"); `/hooks`: "no hooks yet"; `/memory` lists `notebooks/CLAUDE.md` as `@-imported` (after step 5; before it, it didn't) | – |
| 7 | a "Bash command" permission prompt (the transcript may say "Ran 1 shell command" above "Interrupted"; `fab` didn't run) for `fab ls …`; `fab rm …` refused without a prompt | the exact command (`2>&1`, `\| head -100`); a smaller model may first propose `fab exists …`; the block shows as `Error: Permission to use Bash …` or `Not run · permission denied` with `Reason:` |
| 8 | not run in the test | – |
| 9 | `all checks passed` | – |

## What participants get stuck on

- **Trust dialog:** the preselected answer is "No, exit".
- **`/context all` is longer than the window:** scroll up; the categories with their token counts are at the top.
- **No `Loaded` line:** Ctrl+O opens the detailed view, where the line also appears. A single-file shell read such as `cat` or `head` loads the rule too (code.claude.com/docs/en/memory); in the tests Claude always used the Read tool.
- **The import doesn't load:** it has to be outside backticks and code blocks, with `/` also on Windows, and it only applies after a restart (whether `/clear` is enough was not tested).
- **Claude offers to allow the blocked `fab rm`:** an allow rule can't make an exception to a deny rule. That's video 5.
- **MCP tools in `/context all` that nobody configured:** they come from the participant's own account or profile. A good entry for the "Tools" row.

## Check the solution yourself

The files in this folder are one finished run: `CLAUDE.md` with the import from step 5 and the filled-in notes `harness.md`. Put them into a fresh project and `check.py` prints "all checks passed"; on a fresh project without them, it fails. From the exercise folder, in Bash or Git Bash:

```
./setup.sh /var/tmp/04-solved --notes /var/tmp/04-solved-notes
cp solution/CLAUDE.md /var/tmp/04-solved/
cp solution/harness.md /var/tmp/04-solved-notes/
python3 check.py --project /var/tmp/04-solved --notes /var/tmp/04-solved-notes
```

Use new folders each time; setup refuses a folder that already exists.
