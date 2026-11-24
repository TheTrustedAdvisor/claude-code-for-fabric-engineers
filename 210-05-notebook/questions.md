# Questions

`transcript.json` holds three toolkit responses from the recording of part 5. Each one says what state it's in and what to do next. Answer from the responses, not from what you'd expect.

1. **q1, step 1:** `start-session` came back with `status: success`. Is the session ready? What do you run next, with which session id, and when do you stop?
2. **q2, step 2:** `code run` came back with `status: running`. What do you run next, with which execution id? (Submitting the code a second time is the wrong answer.)
3. **q3, step 3:** The local server is stopped. Then Fabric's own API lists the notebook's Livy sessions. Is anything still running? Which command ends it, and how do you know it ended?
4. **open_livy_session:** The `livyId` of the session that's still in progress (the full id, or at least its first eight characters).

Write the answers into `answers.json`, one string per key. Command lines are fine; `check.py` looks for the command and the id, not the exact flags.
