# Answer

- Step 2: Claude computed both numbers with a script over the CSV instead of reading the file into the conversation. The permission prompts showed the script. That keeps 1.1 MB of data out of the context; only the script and its output go in.
- Step 2: Mythenquai counted 61,677 bikes in September 2025; the busiest day was Saturday, 20 September, with 3,586.
- Step 3: run 1 said −29.9 %, run 2 said −28.3 %. The main difference was how each run handled the two counters with missing days.
- Step 4: both independently written scripts printed −28.3 % (weekday sum 23364.0, weekend sum 16753.0). The line that fixed it: "A day counts only if the counter has all 96 quarter hours of that day."
- My rule: a number that has to hold is computed by a script, from decisions written in the prompt, because otherwise Claude decides whatever the question leaves open, run by run.
