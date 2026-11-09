# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Load orders
# Source: `bronze_orders` · Target: `silver_orders`

# CELL ********************

LAST_LOAD = "2026-10-31T23:30:00Z"

orders = spark.read.table("bronze_orders").where(f"order_ts > '{LAST_LOAD}'")
orders.write.mode("append").saveAsTable("silver_orders")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
