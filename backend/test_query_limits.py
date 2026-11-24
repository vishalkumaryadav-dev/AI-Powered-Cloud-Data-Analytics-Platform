import backend.query_engine as query_engine


# Test 1: Maximum result rows
print("\nTesting: 100-row limit")

try:
    query_engine.execute_query(
        "SELECT order_id FROM fact_order_items"
    )
    print("FAILED: More than 100 rows were allowed!")

except ValueError as error:
    print("PASSED:", error)


# Test 2: Query execution timeout
print("\nTesting: Query timeout")

original_timeout = query_engine.QUERY_TIMEOUT_SECONDS

try:
    query_engine.QUERY_TIMEOUT_SECONDS = 0

    query_engine.execute_query("""
        SELECT COUNT(*)
        FROM fact_order_items AS a
        CROSS JOIN fact_order_items AS b
    """)

    print("FAILED: Timeout was not triggered!")

except Exception as error:
    if "interrupted" in str(error).lower():
        print("PASSED: Query execution timeout triggered.")
        print("Reason:", error)
    else:
        print("FAILED: Unexpected error.")
        print("Reason:", error)

finally:
    query_engine.QUERY_TIMEOUT_SECONDS = original_timeout
