from backend.query_engine import execute_query

# Attempt to modify the database
unsafe_query = """
DELETE FROM fact_order_items;
"""

try:
    execute_query(unsafe_query)
    print("WARNING: Unsafe query was executed!")

except Exception as error:
    print("Write operation blocked successfully!")
    print("Error:", error)