
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# Application Header
# -----------------------------------

st.title("📊 AI-Powered E-Commerce Analytics")

st.write(
    "Ask questions about your e-commerce data "
    "and get AI-powered business insights."
)

st.divider()

# -----------------------------------
# Backend API Configuration
# -----------------------------------

API_URL = "http://127.0.0.1:8000/ask"

# -----------------------------------
# User Question Input
# -----------------------------------

st.subheader("Ask Your Business Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Which five product categories generated the highest sales?"
)

ask_button = st.button(
    "Generate Insights",
    type="primary"
)

# -----------------------------------
# Process User Question
# -----------------------------------

if ask_button:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Analyzing your data using Gemini AI..."):

            try:

                # Send question to FastAPI
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=90
                )

                response.raise_for_status()

                data = response.json()

                st.success("Analysis completed successfully!")

                # -----------------------------------
                # Generated SQL
                # -----------------------------------

                st.subheader("Generated SQL")

                st.code(
                    data["generated_sql"],
                    language="sql"
                )

                # -----------------------------------
                # Query Results
                # -----------------------------------

                st.subheader("Query Results")

                results = data["results"]

                if results:

                    df = pd.DataFrame(results)

                    st.metric(
                        "Total Records",
                        data["row_count"]
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    # -----------------------------------
                    # Data Visualization
                    # -----------------------------------

                    numeric_columns = df.select_dtypes(
                        include="number"
                    ).columns.tolist()

                    if len(df.columns) >= 2 and numeric_columns:

                        category_column = df.columns[0]
                        value_column = numeric_columns[0]

                        st.subheader("Data Visualization")

                        fig = px.bar(
                            df,
                            x=category_column,
                            y=value_column,
                            title=(
                                f"{value_column} by "
                                f"{category_column}"
                            ),
                            text=value_column
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                else:

                    st.info("No records found.")

                # -----------------------------------
                # AI-Generated Business Insights
                # -----------------------------------

                st.subheader("🤖 AI-Generated Business Insights")

                st.markdown(data["insights"])

            # -----------------------------------
            # HTTP Error Handling
            # -----------------------------------

            except requests.exceptions.HTTPError as error:

                status_code = error.response.status_code

                if status_code == 400:

                    st.warning(
                        "Your question could not be processed. "
                        "Please ask an e-commerce-related question."
                    )

                else:

                    st.error(
                        f"Backend returned an error: HTTP {status_code}"
                    )

                st.caption(error.response.text)

            # -----------------------------------
            # Connection Error
            # -----------------------------------

            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the backend API. "
                    "Make sure FastAPI is running."
                )

            # -----------------------------------
            # Timeout Error
            # -----------------------------------

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. Please try again."
                )

            # -----------------------------------
            # Other Errors
            # -----------------------------------

            except Exception as error:

                st.error("An unexpected error occurred.")

                st.caption(str(error))


# -----------------------------------
# Footer
# -----------------------------------

st.divider()

st.caption(
    "AI-Powered E-Commerce Analytics Platform | "
    "Built with Python, FastAPI, Gemini, SQLite and Streamlit"
)
