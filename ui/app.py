import streamlit as st
import pandas as pd
import plotly.express as px
import main
import numpy as np

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)
results = main.main()


st.title("Customer Segmentation Dashboard")

rfm = results.get("rfm")
objective_values = results.get("objective_values")

st.subheader("Data Scatter Plot")
fig_3d = px.scatter_3d(
    rfm,
    x="recency",
    y="frequency",
    z="monetary",
    color="cluster",
    hover_data=["customer_id"],
)
st.plotly_chart(fig_3d, use_container_width=True)

st.subheader("Objective Scatter Plot")
data_obj = pd.DataFrame({
    'X_Axis': [c for c in range(1, 11)],
    'Y_Axis': objective_values,
})
fig_obj = px.line(
    data_obj,
    x='X_Axis',
    y='Y_Axis',
    markers= True
)
st.plotly_chart(fig_obj, use_container_width=True)


st.subheader("Customer RFM Data")
st.dataframe(rfm)