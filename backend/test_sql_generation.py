from backend.gemini_service import generate_sql

question = "Which five product categories generated the highest sales?"

sql_query = generate_sql(question)

print("\nGenerated SQL:\n")
print(sql_query)
