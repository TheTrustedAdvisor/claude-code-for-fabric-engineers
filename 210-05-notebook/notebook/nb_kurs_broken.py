# nb_kurs as recorded for part 5: one cell, with the broken date conversion.
# order_date is ISO text (yyyy-MM-dd); the format below reads day first.
# With spark.sql.ansi.enabled false, to_date returns NULL instead of failing, so the job still completes.
import traceback, datetime
from pyspark.sql import functions as F
try:
    df = spark.read.table("orders")
    out = df.groupBy("region").agg({"amount": "sum", "order_id": "count"})
    out = out.withColumnRenamed("sum(amount)", "amount").withColumnRenamed("count(order_id)", "orders")
    out.write.mode("overwrite").format("delta").saveAsTable("orders_by_region")
    days = df.withColumn("day", F.to_date("order_date", "dd.MM.yyyy"))
    by_day = days.groupBy("day").agg(F.count("order_id").alias("orders"), F.round(F.sum("amount"), 2).alias("amount"))
    by_day.write.mode("overwrite").format("delta").saveAsTable("orders_by_day")
    print(by_day.orderBy("day").limit(5).collect())
except Exception:
    stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    mssparkutils.fs.put(f"Files/errors/{stamp}.txt", traceback.format_exc(), True)
    raise
