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

n = spark.read.table("orders_by_region").agg({"orders": "sum"}).first()[0]
assert n == 1000, f"orders_by_region has {n} orders, expected 1000"
print("orders_by_region: 1000 orders")
