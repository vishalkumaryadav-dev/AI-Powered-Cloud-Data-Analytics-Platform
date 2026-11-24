from backend.query_engine import execute_query
from backend.analytics_queries import ANALYTICAL_QUERIES


for query_name, sql_query in ANALYTICAL_QUERIES.items():

    print(f"\n{'=' * 50}")
    print(f"Query: {query_name}")
    print('=' * 50)

    try:
        result = execute_query(sql_query)
        print(result)

    except Exception as error:
        print(f"Query failed: {error}")