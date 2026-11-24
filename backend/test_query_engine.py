
from backend.query_engine import execute_query

# Analytical SQL query
query = """
SELECT
    p.product_category_name,
    SUM(f.total_item_amount) AS revenue
FROM fact_order_items f
JOIN dim_products p
    ON f.product_key = p.product_key
GROUP BY p.product_category_name
ORDER BY revenue DESC
LIMIT 5;
"""

try:
    result = execute_query(query)

    print("Query executed successfully!\n")
    print(result)

    print("\nDataFrame information:")
    result.info()

except Exception as error:
    print("Query execution failed:", error)
