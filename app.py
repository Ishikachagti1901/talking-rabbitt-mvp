import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Page configuration
st.set_page_config(page_title="Talking Rabbitt", layout="wide")

st.title("🐰 Talking Rabbitt")
st.subheader("Talk to your business data")

# Gemini API key from Streamlit secrets
API_KEY = st.secrets["GEMINI_API_KEY"]

# Upload CSV
uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("### Data Preview")
    st.dataframe(df.head())

    # Ask question
    question = st.text_input("Ask a question about your data")

    if question:

        # Calculate useful metrics
        insights = {}

        if "Region" in df.columns and "Revenue" in df.columns:
            insights["revenue_by_region"] = df.groupby("Region")["Revenue"].sum().to_dict()

        if "Month" in df.columns and "Revenue" in df.columns:
            insights["revenue_by_month"] = df.groupby("Month")["Revenue"].sum().to_dict()

        prompt = f"""
You are a business data analyst.

Dataset columns:
{df.columns.tolist()}

Computed statistics from the dataset:
{insights}

User question:
{question}

Provide a short and clear business insight using the numbers above.
"""

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

        body = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:

            response = requests.post(url, json=body)

            result = response.json()

            answer = result["candidates"][0]["content"]["parts"][0]["text"]

            st.write("### Insight")
            st.write(answer)

        except:
            st.error("Failed to get response from Gemini API")

    # Visualization section
    st.write("### Quick Visualization")

    x_col = st.selectbox("X Axis", df.columns)

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        y_col = st.selectbox("Y Axis", numeric_cols)

        fig = px.bar(df, x=x_col, y=y_col, title="Data Visualization")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No numeric columns available for visualization.")