# Fabric notebook cell (PySpark). Attach the lakehouse that holds Files/bikes-2025-09.csv, then run.
# Writes two tables: bike_days (one row per counter and day) and calendar (September 2025 with a day type).
from datetime import date, timedelta

from pyspark.sql import functions as F

raw = spark.read.option("header", True).csv("Files/bikes-2025-09.csv")  # every column as text

# An empty field means "not measured": it adds nothing, and a row with both bike fields empty isn't a measurement.
velo_in = F.when(F.trim(F.col("VELO_IN")) != "", F.col("VELO_IN").cast("long"))
velo_out = F.when(F.trim(F.col("VELO_OUT")) != "", F.col("VELO_OUT").cast("long"))
measured = raw.where(velo_in.isNotNull() | velo_out.isNotNull())

bike_days = (measured
             .withColumn("bikes", F.coalesce(velo_in, F.lit(0)) + F.coalesce(velo_out, F.lit(0)))
             .withColumn("date", F.to_date(F.substring("DATUM", 1, 10)))
             .groupBy(F.col("FK_STANDORT").cast("long").alias("counter_id"), "date")
             .agg(F.sum("bikes").alias("bikes"), F.count("*").alias("quarter_hours")))
bike_days.write.mode("overwrite").format("delta").option("overwriteSchema", "true").saveAsTable("bike_days")

# The team's calendar: Monday 15 September 2025 (Knabenschiessen) is a holiday, not a weekday.
holidays = {date(2025, 9, 15)}
days = [date(2025, 9, 1) + timedelta(days=i) for i in range(30)]
rows = [(d, "holiday" if d in holidays else "weekend" if d.weekday() >= 5 else "weekday") for d in days]
spark.createDataFrame(rows, "date date, day_type string") \
    .write.mode("overwrite").format("delta").option("overwriteSchema", "true").saveAsTable("calendar")

print(spark.table("bike_days").count(), "counter days,", spark.table("calendar").count(), "calendar days")
