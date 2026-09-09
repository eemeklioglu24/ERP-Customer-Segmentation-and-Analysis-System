import streamlit as st
import pandas as pd
import plotly.express as px
import main

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)
results = main.main()

st.title("Customer Segmentation Dashboard")

rfm = results.get("rfm")

st.subheader("Scatter Plot")
fig = px.scatter_3d(
    rfm,
    x="recency",
    y="frequency",
    z="monetary",
    color="cluster",
    hover_data=["customer_id"],
)
st.plotly_chart(fig, use_container_width=True)



st.subheader("Customer RFM Data")
st.dataframe(rfm)