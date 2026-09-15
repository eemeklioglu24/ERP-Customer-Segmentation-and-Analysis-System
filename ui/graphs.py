import plotly.express as px
import pandas as pd
import numpy as np

def get_pca(X_pca, labels, customer_ids, features):
    data_pca = pd.DataFrame({
    "PC1": X_pca[:, 0],
    "PC2": X_pca[:, 1],
    "cluster": labels.astype(str),
    "customer_id": customer_ids,

    "recency": features["recency"].values,
    "monetary": features["monetary"].values,
    "avg_order_value": features["avg_order_value"].values,
    "product_count": features["product_count"].values,
    "transaction_count": features["transaction_count"].values,
    "total_quantity": features["total_quantity"].values
    })
    fig_pca = px.scatter(
        data_pca,
        x="PC1",
        y="PC2",
        color="cluster",
        hover_data=["customer_id","recency","monetary","avg_order_value","product_count","transaction_count","total_quantity"],
    )
    return fig_pca

def get_rfm(features):
    cluster_colors = ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#b15928", "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6", "#ffff99"]
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
    return fig_3d

def get_obj(objective_values):
    data_obj = pd.DataFrame({
    'X_Axis': np.arange(2, 11),
    'Y_Axis': objective_values,
    })
    fig_obj = px.line(
        data_obj,
        x='X_Axis',
        y='Y_Axis',
        markers= True
    )
    return fig_obj

def get_sil(silhouette_scores):
    data_sil = pd.DataFrame({
    'X_Axis': np.arange(2, 11),
    'Y_Axis': silhouette_scores,
    })
    fig_sil = px.line(
        data_sil,
        x='X_Axis',
        y='Y_Axis',
        markers= True
    )
    return fig_sil