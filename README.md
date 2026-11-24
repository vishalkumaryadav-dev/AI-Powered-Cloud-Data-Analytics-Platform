# AI-Powered E-Commerce Data Analytics Platform

An AI-powered analytics application that allows users to ask questions about e-commerce data in natural language and receive SQL-based results, visualizations, and AI-generated business insights.

## Features

- Natural-language analytics using Google Gemini API.
- Automatic SQL query generation.
- Read-only SQLite database access.
- SQL validation and safe query execution.
- FastAPI backend for API services.
- Streamlit frontend for interactive analytics.
- Interactive charts using Plotly.
- AI-generated business insights and recommendations.
- Predefined analytical queries.

## Architecture

Streamlit Frontend → FastAPI Backend → Google Gemini API → SQL Validation → SQLite Data Warehouse → Results and AI Insights.

## Technology Stack

- Python
- SQL
- SQLite
- FastAPI
- Streamlit
- PySpark (Project 1 data pipeline)
- Google Gemini API
- Pandas
- Plotly

## Project Structure

```text
ai-powered-ecommerce-analytics/
├── backend/
│   ├── analytics_queries.py
│   ├── database.py
│   ├── gemini_service.py
│   ├── main.py
│   └── query_engine.py
├── frontend/
│   └── app.py
├── tests/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10 or later
- Google Gemini API key
- Project 1 SQLite database (`ecommerce.db`)

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

5. Make sure the SQLite database is available at the path configured in `backend/database.py`.

## Run the Backend

```bash
uvicorn backend.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

## Run the Frontend

Open another terminal and run:

```bash
streamlit run frontend/app.py
```

## Example Questions

- Which five product categories generated the highest sales?
- How many orders are there for each order status?
- Which products have the highest sales?
- Show sales trends by month.

## Security

- API keys are stored in environment variables.
- `.env` files are excluded from Git.
- Database connections use read-only mode.
- SQL execution is restricted to approved warehouse tables.
- Query execution includes result-size and timeout limits.

## Project Status

Local end-to-end implementation and integration testing completed. Public deployment is planned.

## Author

Vishal Kumar Yadav
