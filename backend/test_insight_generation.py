from backend.gemini_service import generate_insight

question = "Which five product categories generated the highest sales?"

results = [
    {"product_category_name": "beleza_saude", "total_sales": 1441248.07},
    {"product_category_name": "relogios_presentes", "total_sales": 1305541.61},
    {"product_category_name": "cama_mesa_banho", "total_sales": 1241681.72},
    {"product_category_name": "esporte_lazer", "total_sales": 1156656.48},
    {"product_category_name": "informatica_acessorios", "total_sales": 1059272.40}
]

insight = generate_insight(question, results)

print("\nAI-GENERATED BUSINESS INSIGHTS:\n")
print(insight)
