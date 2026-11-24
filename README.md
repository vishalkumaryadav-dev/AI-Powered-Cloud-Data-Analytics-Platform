
# AI-Powered E-Commerce Analytics Platform

An AI-powered e-commerce analytics application that allows users to ask questions about business data in natural language and receive SQL-based results, interactive visualizations, and AI-generated business insights.

## Live Demo

- **Frontend:** https://ai-ecommerce-insights-vk.streamlit.app/
- **Backend API:** https://ai-powered-cloud-data-analytics-platform.onrender.com/
- **API Documentation:** https://ai-powered-cloud-data-analytics-platform.onrender.com/docs

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
- Query execution limits and timeout protection.

## Architecture

```text
             User
              |
              v
     Streamlit Frontend
    (Community Cloud)
              |
              v
       FastAPI Backend
          (Render)
              |
              v
       Google Gemini API
              |
       SQL Generation
              |
              v
       SQL Validation
              |
              v
     SQLite Data Warehouse
              |
        Query Results
              |
              v
       Google Gemini API
              |
       Business Insights
              |
              v
    Results + Charts + Insights
```

## Technology Stack

- Python
- SQL
- SQLite
- FastAPI
- Streamlit
- Google Gemini API
- Pandas
- PySpark (Project 1 data pipeline)
- Plotly
- Git and GitHub
- Render
- Streamlit Community Cloud

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
├── data/
│   └── ecommerce.db.gz
├── tests/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

1. User enters a business question in natural language.
2. Gemini converts the question into an SQL query.
3. Backend validates the generated SQL.
4. SQL executes against the SQLite data warehouse.
5. Query results are returned through FastAPI.
6. Gemini generates business insights based on the results.
7. Streamlit displays SQL, results, charts, and insights.

## Prerequisites

- Python 3.10 or later
- Google Gemini API key
- Git

The repository includes a compressed SQLite database archive in `data/ecommerce.db.gz`. The backend extracts it when the database file is not available.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/vishalkumaryadav-dev/AI-Powered-Cloud-Data-Analytics-Platform.git

cd AI-Powered-Cloud-Data-Analytics-Platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Never upload your API key to GitHub.

### 5. Run the backend

```bash
uvicorn backend.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

### 6. Run the frontend

Open another terminal:

```bash
streamlit run frontend/app.py
```

For local development, configure the frontend API URL as:

```python
API_URL = "http://127.0.0.1:8000/ask"
```

## Example Questions

- What are the top 5 product categories by revenue?
- How many orders are there for each order status?
- Which products have the highest sales?
- Show sales trends by month.
- Which categories generate the most revenue?

## Security and Reliability

- API keys are stored in environment variables.
- `.env` files are excluded from Git.
- Database connections use read-only mode.
- SQL execution is restricted to approved warehouse tables.
- Query execution includes result-size and timeout limits.
- Destructive SQL operations are rejected.

## Deployment

| Component | Platform |
|---|---|
| Frontend | Streamlit Community Cloud |
| Backend | Render |
| Database | SQLite |
| AI Service | Google Gemini API |

The application uses free-tier hosting and API access, subject to provider limits and availability.

**Note:** AWS services are not currently deployed as part of this application.

## Project Status

- Local development completed.
- FastAPI backend deployed successfully.
- Gemini integration verified.
- SQL query execution and validation tested.
- Streamlit frontend deployed successfully.
- Public end-to-end application tested.

## Author

Vishal Kumar Yadav

