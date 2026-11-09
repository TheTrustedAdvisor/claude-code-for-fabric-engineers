# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Bike counts per day
# One row per counting station and day, for the city's traffic report.

# CELL ********************

df = spark.read.table("bike_counts_raw")
daily = df.groupBy("station", "day").sum("bikes_in", "bikes_out")
daily.write.mode("overwrite").saveAsTable("bike_counts_daily")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
