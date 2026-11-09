# Weekend vs weekday, all bike counters

For the transport committee: in September 2025, do more or fewer people cycle on weekends than on weekdays, and by what percentage? Use all bike counters.

Decisions:
- Bikes are VELO_IN plus VELO_OUT, raw counts without the correction factor. An empty field means not measured: skip it, don't count it as 0.
- A day counts only if the counter has all 96 quarter hours of that day.
- Weekdays are Monday to Friday, without Monday 15 September (Knabenschiessen: city offices and schools are closed).
- Weekend days are Saturday and Sunday.
- For each counter, take the mean of its daily totals per day type, rounded to one decimal. Then add up these means over all counters.
- Percentage = weekend sum / weekday sum - 1, times 100, one decimal. Negative means fewer on weekends.

Write a Python script weekend.py that prints the weekday sum, the weekend sum and the percentage, then run it twice. Don't change any other file.
