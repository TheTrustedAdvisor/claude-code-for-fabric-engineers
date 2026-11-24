# Exercise 210-05-notebook

Companion exercise to part 5 of the series "Learning Claude for Microsoft Fabric": "Fabric notebook toolkit: can Claude Code debug a live Spark session?". Runs locally; only the optional steps use your own Fabric workspace.

> **Status:** Ready: `python3 check.py` fails on the empty `answers.json` and passes on `solution/answers.json`.

## Task

The Fabric notebook toolkit (`fntk`, Preview) answers every command with JSON: a `status`, a `stage`, the `data`, and `next_actions` that say what to run next. A response with `status: success` can still mean "not ready yet", and stopping the toolkit's local server doesn't end anything in Fabric.

`transcript.json` holds three responses recorded for the video, with the IDs replaced:

| Step | You ran | What the response says |
|---|---|---|
| 1 | `fntk notebook start-session` | success, but the Livy session is `starting` |
| 2 | `fntk code run` | `running`, with an execution id |
| 3 | `fntk server stop`, then Fabric's Livy sessions API | the server stopped; one session is still `InProgress` |

Work it out with Claude: for each step, the next action, and which session was left open. The questions are in `questions.md`.

## What a good result looks like

```
3 of 3 next actions right
[OK] open session: found a8055483-...
PASS
```

`check.py` reads `answers.json` and grades each answer by the command and the id it names: poll `get-session` for step 1, poll `code get-result` (not `code run` again) for step 2, end the session with `delete-session` and read it back for step 3. A reference is in `solution/answers.json`; look at it after your own attempt.

## How to run it

You need Claude Code and Python 3 as `python3` (standard library only). No capacity, no sign-in.

1. From this folder (`210-05-notebook/` in the companion repo), start `claude`.
2. Ask, for example:

   > Read transcript.json and questions.md. For each step, tell me from the response itself what's finished, what's still running, and the next action with its exact command. Don't run anything. Then write the answers into answers.json.

3. Grade it: `python3 check.py`. With another file: `python3 check.py path/to/answers.json`.

## Optional: the live part

In your own dev workspace, with `fntk` installed and signed in (`python -m pip install fabric-notebook-toolkit ms-fabric-cli`, `fntk init --agent claude`, then `fntk server start`):

1. Load the course seed as the table `orders` in a lakehouse: `python3 ../210-04-verify/states/build.py --csv orders.csv` writes the same 1,000 orders as the video (seed 210, January to March 2026, `order_date` as `yyyy-MM-dd`). Upload it and load it as a table.
2. Create a notebook `nb_kurs` with that lakehouse as default and paste `notebook/nb_kurs_broken.py` as its cell. It runs, completes, and writes `orders_by_day` with an empty day: the format reads day first.
3. Let Claude find and fix it as in the video: read only first, then a session, then the edit, then a job run. Approve each step.
4. End every session you started, and read it back. Then check that nothing is left open:
   ```
   python3 check.py --live -w <workspace id> -a <notebook id>
   ```
   It passes the live line only if `fntk notebook list-sessions` lists no active session for that notebook. The Fabric monitor hub shows the same, a little later. Pause or stop your capacity when you're done.
