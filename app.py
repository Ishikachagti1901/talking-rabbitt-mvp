import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Talking Rabbitt 🐰")
st.subheader("Ask questions to your business data")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.write("### Data Preview")
    st.dataframe(df)

    question = st.text_input("Ask a question")

    if question:

        q = question.lower()

        if "highest revenue" in q:

            result = df.groupby("Region")["Revenue"].sum()
            top_region = result.idxmax()
            top_value = result.max()

            st.success(f"{top_region} has the highest revenue: {top_value}")

            st.write("### Revenue by Region")
            result.plot(kind="bar")

            st.pyplot(plt)

        elif "total revenue" in q:

            total = df["Revenue"].sum()
            st.success(f"Total revenue is {total}")

        elif "trend" in q:

            result = df.groupby("Month")["Revenue"].sum()

            st.write("### Revenue Trend")
            result.plot()

            st.pyplot(plt)

        else:
            st.warning("Try asking: highest revenue, total revenue, or revenue trend.")