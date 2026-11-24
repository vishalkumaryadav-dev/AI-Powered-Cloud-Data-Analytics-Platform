ANALYTICAL_QUERIES = {
    "top_products": """
        SELECT
            p.product_category_name,
            SUM(f.total_item_amount) AS total_amount
        FROM fact_order_items f
        JOIN dim_products p
            ON f.product_key = p.product_key
        GROUP BY p.product_category_name
        ORDER BY total_amount DESC
        LIMIT 5;
    """,

    "order_status": """
        SELECT
            order_status,
            COUNT(DISTINCT order_id) AS total_orders
        FROM fact_order_items
        GROUP BY order_status
        ORDER BY total_orders DESC;
    """,

    "state_sales": """
        SELECT
            c.customer_state,
            SUM(f.total_item_amount) AS total_amount
        FROM fact_order_items f
        JOIN dim_customers c
            ON f.customer_key = c.customer_key
        GROUP BY c.customer_state
        ORDER BY total_amount DESC
        LIMIT 5;
    """
}