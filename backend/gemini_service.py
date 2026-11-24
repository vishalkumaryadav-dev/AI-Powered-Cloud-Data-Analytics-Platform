import json
import os

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Selected Gemini model
MODEL_NAME = "gemini-3.5-flash-lite"


def generate_sql(question: str) -> str:
    """
    Convert a natural-language question into an SQL query.
    """

    prompt = f"""
    You are an expert SQL developer working with an e-commerce SQLite database.

    Your task is to convert the user's question into a SQLite SQL query.

    DATABASE SCHEMA:

    Table: fact_order_items
    Columns:
    - order_item_fact_key
    - order_id
    - order_item_id
    - customer_key
    - product_key
    - seller_key
    - order_date_key
    - order_status
    - price
    - freight_value
    - total_item_amount

    Table: dim_customers
    Columns:
    - customer_key
    - customer_id
    - customer_unique_id
    - customer_city
    - customer_state

    Table: dim_products
    Columns:
    - product_key
    - product_id
    - product_category_name
    - product_name_length
    - product_description_length
    - product_photos_qty
    - product_weight_g
    - product_length_cm
    - product_height_cm
    - product_width_cm

    Table: dim_sellers
    Columns:
    - seller_key
    - seller_id
    - seller_city
    - seller_state

    Table: dim_date
    Columns:
    - date_key
    - full_date
    - day
    - month
    - year
    - quarter
    - day_of_week

    TABLE RELATIONSHIPS:

    - fact_order_items.customer_key = dim_customers.customer_key
    - fact_order_items.product_key = dim_products.product_key
    - fact_order_items.seller_key = dim_sellers.seller_key
    - fact_order_items.order_date_key = dim_date.date_key

    IMPORTANT RULES:

    1. Generate SQLite-compatible SQL only.
    2. Generate only one SELECT query.
    3. Do not generate INSERT, UPDATE, DELETE, DROP or ALTER statements.
    4. Do not generate PRAGMA or ATTACH statements.
    5. Do not use tables or columns outside the schema.
    6. Use appropriate JOINs when information comes from multiple tables.
    7. Use LIMIT 100 for queries that could return many rows.
    8. Do not include Markdown formatting or explanations.
    9. total_item_amount includes item price plus freight_value.

    USER QUESTION:
    {question}

    Return only the SQL query.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return response.text.strip()


def generate_insight(question: str, results: list[dict]) -> str:
    """
    Generate business insights from SQL query results.
    """

    prompt = f"""
    You are a professional e-commerce business data analyst.

    Analyze the SQL query results and provide useful business insights.

    USER QUESTION:
    {question}

    QUERY RESULTS:
    {json.dumps(results, indent=2)}



INSTRUCTIONS:
1. Explain the important findings in simple language.
2. Highlight the highest and lowest values when relevant.
3. Identify meaningful patterns supported by the query results.
4. Provide 2-3 actionable business recommendations.
5. Use only the information present in the results.
6. Never invent facts, statistics, trends, or customer behavior.
7. Clearly distinguish observed findings from recommendations.
8. Never assume a currency symbol or currency unit.
   Refer to numeric values as sales amounts unless the
   currency is explicitly provided.
9. Do not claim that inventory levels, customer demand,
   profit, or stock availability are known unless the
   supplied results directly establish them.
10. Keep the response concise and well-structured.
11. Never infer the cause of an order status, cancellation,
    unavailable order, or business outcome from counts alone.

12. Do not describe statuses as a sequential pipeline or
    assume that orders transition between statuses.

13. Do not label orders as successful, failed, active, or
    delayed unless the supplied data directly supports it.

14. Clearly distinguish:
    - Observed facts: directly supported by query results.
    - Possible explanations: explicitly label as hypotheses.
    - Recommendations: suggestions, not proven conclusions.


Return the business insights only.

    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty insight")

    return response.text.strip()
