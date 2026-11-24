

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.analytics_queries import ANALYTICAL_QUERIES
from backend.query_engine import execute_query
from backend.gemini_service import generate_sql, generate_insight


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title="AI-Powered E-Commerce Analytics API",
    description="Backend API for AI-powered e-commerce data analytics",
    version="1.0.0"
)


# Existing request structure
class QueryRequest(BaseModel):
    query_name: str


# New request structure for natural-language questions
class NaturalLanguageQueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI-Powered E-Commerce Analytics API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Backend"
    }


# Existing analytical query endpoint
@app.post("/query")
def query_data(request: QueryRequest):

    if request.query_name not in ANALYTICAL_QUERIES:
        raise HTTPException(
            status_code=400,
            detail="Invalid query name"
        )

    sql_query = ANALYTICAL_QUERIES[request.query_name]

    try:
        result_df = execute_query(sql_query)
        results = result_df.to_dict(orient="records")

        return {
            "query_name": request.query_name,
            "row_count": len(results),
            "results": results
        }

    except Exception:
        logger.exception("Error executing analytical query")

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while executing the query"
        )


# New AI-powered natural-language endpoint
@app.post("/ask")
def ask_question(request: NaturalLanguageQueryRequest):

    # Step 1: Generate SQL using Gemini
    try:
        sql_query = generate_sql(request.question)

    except Exception:
        logger.exception("Gemini SQL generation failed")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate SQL using Gemini"
        )

    # Step 2: Safely execute generated SQL
    try:
        result_df = execute_query(sql_query)
        results = result_df.to_dict(orient="records")

    except Exception:
        logger.exception("Generated SQL execution failed")

        raise HTTPException(
            status_code=400,
            detail="Generated SQL could not be safely executed"
        )

    # Step 3: Generate business insights using Gemini
    try:
        insights = generate_insight(
            request.question,
            results
        )

    except Exception:
        logger.exception("AI insight generation failed")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate business insights"
        )

    # Step 4: Return complete response
    return {
        "question": request.question,
        "generated_sql": sql_query,
        "row_count": len(results),
        "results": results,
        "insights": insights
    }
