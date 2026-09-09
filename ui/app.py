import streamlit as st
import pandas as pd
import plotly.express as px
import main
import numpy as np

# Initialization
st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)

st.title("Customer Segmentation Dashboard")
# K slider
k = st.slider(
    "Number of customer segments",
    min_value=2,
    max_value=10,
    value=4
)
        #results = main.main()
results = main.main(K=k)
rfm = results.get("rfm")
objective_values = results.get("objective_values")

# 3D RFM Graph
cluster_colors = ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#b15928",
                               "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6", "#ffff99"]
st.subheader("Data Scatter Plot")
rfm["cluster"] = rfm["cluster"].astype(str)
fig_3d = px.scatter_3d(
    rfm,
    x="recency",
    y="frequency",
    z="monetary",
    color="cluster",
    hover_data=["customer_id"],
    color_discrete_sequence=cluster_colors
)
fig_3d.update_traces(
    marker=dict(
        size=5,
        opacity=0.9
    )
)
st.plotly_chart(fig_3d, use_container_width=True)

# Cluster Profiling
cluster_profile = (
    rfm.groupby("cluster")
    .agg(
        customers=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean")
    )
    .reset_index()
)

st.subheader("Cluster Profiles")
st.dataframe(cluster_profile)

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(rfm))
col2.metric("Number of Segments", rfm["cluster"].nunique())
col3.metric("Total Revenue", f"{rfm['monetary'].sum():,.0f} ₺")

# Objective Graph
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

# RFM csv
selected_cluster = st.selectbox(
    "Select Customer Segment",
    ["All"] + sorted(rfm["cluster"].astype(str).unique().tolist())
)

if selected_cluster == "All":
    displayed = rfm
else:
    displayed = rfm[
        rfm["cluster"].astype(str) == selected_cluster
    ]

st.dataframe(displayed)