
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("NIFTY50 Quant Research Dashboard")

uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.dataframe(df.head())

    fig = px.line(df, y="Close")

    st.plotly_chart(fig)
