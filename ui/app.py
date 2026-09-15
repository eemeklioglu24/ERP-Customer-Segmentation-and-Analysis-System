import streamlit as st
import pandas as pd
import plotly.express as px
import main
import numpy as np

# Initialization
# The command is python -m streamlit run ui/app.py

st.set_page_config(
    page_title="Müşteri Kümeleştirmesi",
    layout="wide"
)

st.title("Müşteri Segmentasyonu Kontrol Paneli")
# K slider
k = st.slider(
    "Küme Sayısı",
    min_value=2,
    max_value=10,
    value=4
)
        #results = main.main()
results = main.main(K=k)
# rfm = results.get("rfm")
features = results.get("features")
objective_values = results.get("objective_values")

# 3D RFM Graph
cluster_colors = ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#b15928",
                               "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6", "#ffff99"]
st.subheader("Müşteri Verileri")
features["cluster"] = features["cluster"].astype(str)
fig_3d = px.scatter_3d(
    features,
    x="recency",
    y="transaction_count",
    z="monetary",
    color="cluster",
    hover_data=["customer_id"],
    color_discrete_sequence=cluster_colors
)
fig_3d.update_layout(
    width=1000,
    height=1000,
)
fig_3d.update_traces(
    marker=dict(
        size=5,
        opacity=0.9
    )
)
col1, col2, col3 = st.columns([1 , 3, 1])

with col1, col3:
    st.write("")
with col2:
    st.plotly_chart(fig_3d, use_container_width=True)

# Cluster Profiling
for insight in results["cluster_insights"]:

    st.markdown(f"## Küme {insight['cluster']} — {insight['segment_name']}")

    st.write(
        f"**{insight['recency_level'].capitalize()} alımlar · "
        f"{insight['frequency_level'].capitalize()} frekans · "
        f"{insight['monetary_level'].capitalize()} parasal değer**"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Ortalama en son siparişten geçen süre",
            f"{insight['recency']:.0f} gün"
        )

    with col2:
        st.metric(
            "Ortalama frekans",
            f"{insight['frequency']:.1f}"
        )

    with col3:
        st.metric(
            "Ortalama parasal değer",
            f"{insight['monetary']:,.0f}₺"
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Müşteri Sayısı",
            f"{insight['customer_count']}"
        )

    with col5:
        st.metric(
            "Toplam Parasal Değer",
            f"{insight['total_monetary']:,.0f}₺"
        )

    with col6:
        st.metric(
            "Toplamdaki Pay",
            f"%{insight['monetary_share']:.1f}"
        )

    st.divider()

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Müşteri Sayısı", len(features))
col2.metric("Küme Sayısı", features["cluster"].nunique())
col3.metric("Toplam Kazanç", f"{features['monetary'].sum():,.0f} ₺")

# Objective Graph
st.subheader("Hedef - Küme grafiği")
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
    "Müşteri kümesini seçiniz",
    ["All"] + sorted(features["cluster"].astype(str).unique().tolist())
)

if selected_cluster == "All":
    displayed = features
else:
    displayed = features[
        features["cluster"].astype(str) == selected_cluster
    ]

st.dataframe(displayed)