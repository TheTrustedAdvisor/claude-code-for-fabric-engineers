"""Clean the raw bike counts before they go to the lakehouse.

    python3 clean_counts.py raw.csv clean.csv
"""
import csv
import sys

COUNT_COLUMNS = ["bikes_in", "bikes_out"]


def clean(row):
    for column in COUNT_COLUMNS:
        value = row.get(column, "").strip()
        row[column] = value if value.isdigit() else "0"
    return row


if __name__ == "__main__":
    source, target = sys.argv[1], sys.argv[2]
    with open(source, newline="", encoding="utf-8") as raw, open(target, "w", newline="", encoding="utf-8") as out:
        reader = csv.DictReader(raw)
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow(clean(row))
