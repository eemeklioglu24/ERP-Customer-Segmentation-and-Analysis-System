import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

import graphs
import main
from src.erp import logo_erp
from ui.database_setup import database_setup
from ui.table_setup import table_selection
from src.functions import test_robustness


if "stage" not in st.session_state:
    st.session_state["stage"] = "connection"


# --------------------------------
# STAGE 1: DATABASE CONNECTION
# --------------------------------

if st.session_state["stage"] == "connection":
    st.title("Database Connection")
    db_config = database_setup()
    if db_config is not None:
        st.session_state["stage"] = "table_selection"
        st.rerun()
    st.stop()


# --------------------------------
# STAGE 2: DATA SOURCE
# --------------------------------

if st.session_state["stage"] == "table_selection":
    st.title("Data Source Selection")
    table_config = table_selection(
        st.session_state["db_config"]
    )
    if table_config is not None:
        st.session_state["stage"] = "dashboard"
        st.rerun()
    st.stop()


# --------------------------------
# STAGE 3: DASHBOARD
# --------------------------------

if st.session_state["stage"] == "dashboard":
    st.title("Customer Segmentation Dashboard")
    db_config = st.session_state["db_config"]
    table_config = st.session_state["table_config"]

    if st.button("ERP Verilerini Yenileme"):
        erp = logo_erp.LogoERP(table_config)
        erp.refresh_features(db_config)
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

    # CLUSTERING SETTINGS
    st.header("Kümeleştirme Ayarları")
    k = st.slider(
        "Küme Sayısı",
        min_value=2,
        max_value=10,
        value=4
    )
            #results = main.main()
    results = main.main(K=k, n_init=5)
    features = results.get("features"); X = results.get("X"); X_pca = results.get("X_pca")
    customer_ids = results.get("customer_ids"); labels = results.get("memberships"); centroids = results.get("centroids")
    objective_values = results.get("objective_values"); silhouette_scores = results.get("silhouette_scores")
    K = results.get("K"); cluster_insights = results.get("cluster_insights")

        # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Müşteri Sayısı", len(features))
    col2.metric("Küme Sayısı", features["cluster"].nunique())
    col3.metric("Toplam Kazanç", f"{features['monetary'].sum():,.0f} ₺")

    # MODEL EVALUATION
    st.header("Model Değerlendirmeleri")

        # Objective Graph
    st.subheader("Hedef - Küme Grafiği")
    fig_obj = graphs.get_obj(objective_values)
    st.plotly_chart(fig_obj, width="stretch")

        # Silhouette Graph
    st.subheader("Silüet Grafiği")
    fig_sil = graphs.get_sil(silhouette_scores)
    st.plotly_chart(fig_sil, width="stretch")

    # ROBUSTNESS ANALYSIS
    st.header("Dayanıklılık Analizi")
    if st.button("Run Robustness Test"):

        objectives, silhouettes = test_robustness(X, len(X), K, n_runs=20)

        objective_mean = np.mean(objectives); objective_std = np.std(objectives)
        silhouette_mean = np.mean(silhouettes); silhouette_std = np.std(silhouettes)
        silhouette_min = np.min(silhouettes); silhouette_max = np.max(silhouettes)
        objective_min = np.min(objectives); objective_max = np.max(objectives)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Mean Silhouette", f"{silhouette_mean:.3f}")
            st.metric("Silhouette Std", f"{silhouette_std:.3f}")

        with col2:
            st.metric("Mean Objective", f"{objective_mean:.2f}")
            st.metric("Objective Std", f"{objective_std:.2f}")

        st.write(f"Silhouette range: " f"{silhouette_min:.3f} – {silhouette_max:.3f}")
        st.write(f"Objective range: " f"{objective_min:.2f} – {objective_max:.2f}")
        fig_rob = graphs.get_rob(silhouettes, silhouette_mean, K)
        st.plotly_chart(fig_rob, width="stretch")

    # PCA VISALISATION
    st.header("PCA Grafiği")
        # PCA Graph
    fig_pca = graphs.get_pca(X_pca, labels, customer_ids, features)
    st.plotly_chart(fig_pca, width="stretch")

    # CLUSTER INTERPRETATIONS
    st.header("Küme Değerlendirmeleri")
    for insight in results["cluster_insights"]:
        st.markdown(f"## Küme {insight['cluster']} — {insight['segment_name']}")

        st.write(
                f"**Güncellik:** {insight['recency_level']}  |  "
                f"**Frekans:** {insight['frequency_level']}  |  "
                f"**Parasal Değer:** {insight['monetary_level']}  |  "
                f"**Ortalama Sipariş Değeri:** {insight['avg_order_value_level']}  |  "
                f"**Ortalama Ürün Sayısı:** {insight['product_count_level']}  |  "
                f"**Toplam Ürün Sayısı:** {insight['total_quantity_level']}"
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Ortalama en son siparişten geçen süre", f"{insight['recency']:.0f} gün")
        col2.metric("Ortalama frekans", f"{insight['frequency']:.1f}")
        col3.metric("Ortalama parasal değer", f"{insight['monetary']:,.0f}₺")

        col4, col5, col6 = st.columns(3)
        col4.metric(f"Ortalama Sipariş Değeri ({insight['avg_order_value_level']})", f"{insight['avg_order_value']:.2f}")
        col5.metric(f"Ortalama Ürün Sayısı ({insight['product_count_level']})", f"{insight['product_count']:.1f}")
        col6.metric(f"Toplam Ürün Sayısı ({insight['total_quantity_level']})", f"{insight['total_quantity']:.1f}")

        col7, col8, col9 = st.columns(3)
        col7.metric("Müşteri Sayısı", f"{insight['customer_count']}")
        col8.metric("Toplam Parasal Değer", f"{insight['total_monetary']:,.0f}₺")
        col9.metric("Toplamdaki Pay", f"%{insight['monetary_share']:.1f}")

        st.divider()

    # X csv
    st.subheader("Müşteri Verileri")
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