# Solution notes for exercise 1

For instructors and for checking your own run. Fixed values come from the data; everything Claude writes freely varies from run to run.

| Step | Fixed | Varies |
|---|---|---|
| 2 | Mythenquai, raw counts: 61,677 bikes; busiest day Saturday, 20 September 2025, 3,586 bikes. With the correction factor 0.98: about 60,443 and 3,514. | Wording; whether Claude mentions the correction factor (in the test it did, as "Decision for you"); the exact script. |
| 3 | Fewer bikes on weekends. | The percentage. Four test runs (Opus): −29.9 %, −28.3 %, −24.5 %, −24.5 %. Each list named 17 or 18 decisions. |
| 4 | With [`prompt-2.md`](prompt-2.md): weekday sum 23,364.0, weekend sum 16,753.0, −28.3 %, in both independently written scripts. | Script layout and output format (for example `-28.3 %` or `-28.3%`); `check.py` compares the numbers only. |
| 6 | With [`../fabric/measures.dax`](../fabric/measures.dax) on the tables from [`../fabric/load_bike_days.py`](../fabric/load_bike_days.py): weekday 23,364.0, weekend 16,753.1, −28.3. The weekend sum differs from Python by 0.1 (Bucheggplatz 1,076.25: Python rounds to even, DAX away from zero). | – |

Files: [`prompt.md`](prompt.md) (step 2), [`prompt-2.md`](prompt-2.md) and [`weekend.py`](weekend.py) (step 4, the first script from the test run), [`results/`](results/) (steps 2, 3 and 5).

Two things worth asking in a debrief:

- In step 3, one run said −28.3 % with Monday 15 September as a weekday, the same headline as the solution's decisions with 15 September as a holiday (weekday sums 23,377.1 and 23,364.0). The same number from different decisions is luck, not a definition.
- In another test run, Claude put Knabenschiessen on Monday 8 September. The date isn't in the data; it came from the model's training. Writing it into `prompt-2.md` is what makes it a decision.

Why `check.py` stays outside the project: inside it, Claude would read the expected values.

## Check the solution yourself

The files in this folder are one finished run: `results/`, `prompt-2.md` and `weekend.py`. Put them into a fresh project and `check.py` prints "all checks passed"; on a fresh project without them, it fails. From the exercise folder, in Bash or Git Bash:

```
./setup.sh /var/tmp/01-solved
cp -r solution/results solution/prompt-2.md solution/weekend.py /var/tmp/01-solved/
mkdir -p /var/tmp/01-solved-keep && cp solution/weekend.py /var/tmp/01-solved-keep/weekend-1.py
python3 check.py --project /var/tmp/01-solved --first /var/tmp/01-solved-keep/weekend-1.py
```

Use new folders each time; setup refuses a folder that already exists.
