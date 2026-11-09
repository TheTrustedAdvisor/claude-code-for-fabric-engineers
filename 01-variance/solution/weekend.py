"""Weekend vs weekday cycling, all bike counters, September 2025.

Reads bikes-2025-09.csv and counters.csv (read-only) and prints the
weekday sum, the weekend sum and the weekend-vs-weekday percentage.
"""
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDED = {date(2025, 9, 15)}  # Knabenschiessen

# Bike counters: velo == 1 in counters.csv (excludes pure pedestrian counters).
with open(HERE / "counters.csv", newline="", encoding="utf-8") as f:
    bike_counters = {row["id1"] for row in csv.DictReader(f) if row["velo"] == "1"}

totals = defaultdict(int)       # (counter, day) -> bikes
quarters = defaultdict(set)     # (counter, day) -> quarter hours seen
with open(HERE / "bikes-2025-09.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cid = row["FK_STANDORT"]
        if cid not in bike_counters:
            continue
        ts = row["DATUM"]
        day = date.fromisoformat(ts[:10])
        if (day.year, day.month) != (2025, 9):
            continue
        # Empty field = not measured: skip it, don't count as 0.
        bikes = sum(int(row[k]) for k in ("VELO_IN", "VELO_OUT") if row[k] != "")
        totals[(cid, day)] += bikes
        quarters[(cid, day)].add(ts[11:16])

# Daily totals per counter and day type, complete days only.
daily = defaultdict(lambda: {"weekday": [], "weekend": []})
for (cid, day), total in totals.items():
    if len(quarters[(cid, day)]) != 96:
        continue
    if day.weekday() >= 5:
        daily[cid]["weekend"].append(total)
    elif day not in EXCLUDED:
        daily[cid]["weekday"].append(total)

weekday_sum = weekend_sum = 0.0
for cid in sorted(daily):
    if daily[cid]["weekday"]:
        weekday_sum += round(sum(daily[cid]["weekday"]) / len(daily[cid]["weekday"]), 1)
    if daily[cid]["weekend"]:
        weekend_sum += round(sum(daily[cid]["weekend"]) / len(daily[cid]["weekend"]), 1)

weekday_sum = round(weekday_sum, 1)
weekend_sum = round(weekend_sum, 1)
pct = round((weekend_sum / weekday_sum - 1) * 100, 1)

print(f"Weekday sum: {weekday_sum:.1f}")
print(f"Weekend sum: {weekend_sum:.1f}")
print(f"Percentage:  {pct:+.1f} %")
