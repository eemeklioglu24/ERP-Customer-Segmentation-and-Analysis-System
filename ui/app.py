import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

import graphs
import main
from src.erp import logo_erp

# Initialization
# The command is python -m streamlit run ui/app.py
if st.button("Refresh ERP Data"):
    erp = logo_erp.LogoERP()
    erp.refresh_features()
    st.success("Customer features refreshed.")
    st.rerun()


FEATURE_PATH = Path("docs/Customer Features.csv")
if not FEATURE_PATH.exists():
    st.warning(
        "No local customer feature snapshot exists yet. "
        "Press 'Refresh ERP Data' to create one."
    )

    st.stop()

st.set_page_config(page_title="Müşteri Kümeleştirmesi",layout="wide")
st.title("Müşteri Segmentasyonu Kontrol Paneli")

# K slider
k = st.slider(
    "Küme Sayısı",
    min_value=2,
    max_value=10,
    value=4
)
        #results = main.main()
results = main.main(K=k, n_init=5)
# rfm = results.get("rfm")
features = results.get("features")
objective_values = results.get("objective_values")
silhouette_scores = results.get("silhouette_scores")
X_pca = results.get("X_pca")
labels = results.get("memberships")
customer_ids = results.get("customer_ids")
centroids = results.get("centroids")

# PCA Graph
st.subheader("PCA Grafiği")
fig_pca = graphs.get_pca(X_pca, labels, customer_ids, features)
st.plotly_chart(fig_pca, width="stretch")

# 3D RFM Graph
st.subheader("Müşteri Verileri")
fig_3d = graphs.get_rfm(features)
col1, col2, col3 = st.columns([1 , 3, 1])
with col1, col3:
    st.write("")
with col2:
    st.plotly_chart(fig_3d, width="stretch")

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
st.subheader("Hedef - Küme Grafiği")
fig_obj = graphs.get_obj(objective_values)
st.plotly_chart(fig_obj, width="stretch")

# Silhouette Graph
st.subheader("Silüet Grafiği")
fig_sil = graphs.get_sil(silhouette_scores)
st.plotly_chart(fig_sil, width="stretch")

# X csv
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