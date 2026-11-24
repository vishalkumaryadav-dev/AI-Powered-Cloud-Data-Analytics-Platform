from backend.query_engine import execute_query


test_queries = {
    "Unauthorized table": """
        SELECT * FROM sqlite_master;
    """,

    "Dangerous function": """
        SELECT load_extension('malicious.so');
    """,

    "Multiple SQL statements": """
        SELECT COUNT(*) FROM fact_order_items;
        SELECT COUNT(*) FROM dim_products;
    """
}


for test_name, query in test_queries.items():

    print(f"\nTesting: {test_name}")

    try:
        execute_query(query)
        print("FAILED: Unsafe query was allowed!")

    except Exception as error:
        print("PASSED: Unsafe query blocked.")
        print("Reason:", error)
