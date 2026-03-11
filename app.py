import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

# Page setup
st.set_page_config(page_title="Talking Rabbitt", layout="wide")

st.title("🐰 Talking Rabbitt")
st.subheader("Talk to your business data")

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
    default_headers={
        "HTTP-Referer": "https://talking-rabbitt.streamlit.app",
        "X-Title": "Talking Rabbitt"
    }
)

# Upload CSV
uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("### Data Preview")
    st.dataframe(df.head())

    # Ask question
    question = st.text_input("Ask a question about your data")

    if question:

        prompt = f"""
You are a business data analyst.

Dataset columns:
{df.columns.tolist()}

Sample data:
{df.head(5).to_string()}

User question:
{question}

Give a short, clear answer based on the dataset.
"""

        try:

            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )

            answer = response.choices[0].message.content

            st.write("### Insight")
            st.write(answer)

        except Exception as e:
            st.error("AI request failed. Check API key or model.")
            st.write(e)

    # Visualization section
    st.write("### Quick Visualization")

    x_col = st.selectbox("X Axis", df.columns)

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        y_col = st.selectbox("Y Axis", numeric_cols)

        fig = px.bar(df, x=x_col, y=y_col)

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No numeric columns available for visualization.")