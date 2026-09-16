import pandas as pd

def classify_z(value):
    # General Classifier
    if value < -1.0:
        return "çok düşük"
    elif value < -0.5:
        return "düşük"
    elif value <= 0.5:
        return "orta"
    elif value <= 1.0:
        return "yüksek"
    else:
        return "çok yüksek"

def classify_recency_z(value):
    # Recency is Inverted
    if value < -0.5:
        return "yakın tarihli"
    elif value > 0.5:
        return "pasif"
    else:
        return "nispeten yakın tarihli"

def interpret_cluster(row):
    # Interprets a single cluster
    recency_level = classify_recency_z(row["recency_z"])
    frequency_level = classify_z(row["frequency_z"])
    monetary_level = classify_z(row["monetary_z"])
    avg_order_value_level = classify_z(row["avg_order_value_z"])
    product_count_level = classify_z(row["product_count_z"])
    total_quantity_level = classify_z(row["total_quantity_z"])

    segment_name = get_segment_name(
        recency_level,
        frequency_level,
        monetary_level
    )
    return{
        "cluster": int(row["cluster"]),
        "segment_name": segment_name,

        "recency_level": recency_level,
        "frequency_level": frequency_level,
        "monetary_level": monetary_level,
        "avg_order_value_level": avg_order_value_level,
        "product_count_level": product_count_level,
        "total_quantity_level": total_quantity_level,

        "recency": row["recency"],
        "frequency": row["frequency"],
        "monetary": row["monetary"],
        "avg_order_value": row["avg_order_value"],
        "product_count": row["product_count"],
        "total_quantity": row["total_quantity"],

        "customer_count": int(row["customer_count"]),
        "total_monetary": row["total_monetary"],
        "monetary_share": row["monetary_share"]
    }

def get_segment_name(recency_level, frequency_level, monetary_level):
    # This code is so ass
    high_levels = ["yüksek", "çok yüksek"]
    low_levels = ["düşük", "çok düşük"]

    if frequency_level in high_levels and monetary_level in high_levels:
        if recency_level == "pasif":
            return "Risk Altındaki Yüksek Harcamalı Müşteriler"
        else:
            return "Yüksek Harcamalı Aktif Müşteriler"

    if frequency_level in low_levels and monetary_level in low_levels:
        if recency_level == "pasif":
            return "Pasif Düşük Harcamalı Müşteriler"
        else:
            return "Yakın Dönemde Alım Yapan Düşük Etkileşimli Müşteriler"

    if monetary_level in high_levels and frequency_level not in high_levels:
        return "Yüksek Harcamalı Seyrek Müşteriler"

    if frequency_level in high_levels and monetary_level not in high_levels:
        return "Sık Alım Yapan Müşteriler"

    return "Orta Değerli Müşteriler"

def interpret(cluster_data: pd.DataFrame, features_clustered: pd.DataFrame):
    # Interprets all clusters
    interpretations = []

    cluster_stats = (
    features_clustered
    .groupby("cluster")
    .agg( customer_count=("customer_id", "count"), total_monetary=("monetary", "sum")).reset_index())

    cluster_stats["monetary_share"] = (cluster_stats["total_monetary"] / cluster_stats["total_monetary"].sum() * 100)
    
    cluster_data = cluster_data.merge(cluster_stats, on="cluster", how="left")

    for _, row in cluster_data.iterrows():
        interpretations.append(
            interpret_cluster(row)
        )
    return interpretations