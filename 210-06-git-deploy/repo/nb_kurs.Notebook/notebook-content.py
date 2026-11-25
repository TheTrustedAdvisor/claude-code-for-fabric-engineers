# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0487129d-f566-48c6-8449-26dfa77b3853",
# META       "default_lakehouse_name": "lh_kurs",
# META       "default_lakehouse_workspace_id": "b296d542-9719-4227-be31-76cc101c40c5"
# META     }
# META   }
# META }

# CELL ********************

df = spark.read.table("orders")
out = df.groupBy("region").agg({"amount": "sum", "order_id": "count"})
out = out.withColumnRenamed("sum(amount)", "amount").withColumnRenamed("count(order_id)", "orders")
out.write.mode("overwrite").format("delta").saveAsTable("orders_by_region")
