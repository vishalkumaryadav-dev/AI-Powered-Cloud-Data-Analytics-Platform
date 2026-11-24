from backend.database import get_db_connection

connection = get_db_connection()
cursor = connection.cursor()

tables = [
    "dim_customers",
    "dim_products",
    "dim_sellers",
    "dim_date",
    "fact_order_items"
]

for table in tables:
    print(f"\nTable: {table}")

    cursor.execute(f"PRAGMA table_info({table})")

    columns = cursor.fetchall()

    for column in columns:
        print(column["name"], "-", column["type"])

connection.close()
