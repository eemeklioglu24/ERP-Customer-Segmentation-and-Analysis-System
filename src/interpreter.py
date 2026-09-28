import pandas as pd

def classify_z(value):
    # General classifier for standardized feature values

    if value < -1.25:
        return "çok düşük"
    elif value < -0.50:
        return "düşük"
    elif value < -0.15:
        return "hafif düşük"
    elif value <= 0.15:
        return "orta"
    elif value <= 0.50:
        return "hafif yüksek"
    elif value <= 1.25:
        return "yüksek"
    else:
        return "çok yüksek"


def classify_recency_z(value):
    # Recency is inverted:
    # lower recency = more recent customer activity

    if value < -1.25:
        return "çok yakın tarihli"
    elif value < -0.50:
        return "yakın tarihli"
    elif value < -0.15:
        return "nispeten yakın tarihli"
    elif value <= 0.15:
        return "ortalama"
    elif value <= 0.50:
        return "nispeten pasif"
    elif value <= 1.25:
        return "pasif"
    else:
        return "çok pasif"

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


def get_segment_name(recency_level, frequency_level, monetary_level,):
    
    LEVEL_SCORE = {
        "çok düşük": -3,
        "düşük": -2,
        "hafif düşük": -1,
        "orta": 0,
        "hafif yüksek": 1,
        "yüksek": 2,
        "çok yüksek": 3,
    }

    RECENCY_SCORE = {
        "çok yakın tarihli": -3,
        "yakın tarihli": -2,
        "nispeten yakın tarihli": -1,
        "ortalama": 0,
        "nispeten pasif": 1,
        "pasif": 2,
        "çok pasif": 3,
    }
    recency = RECENCY_SCORE[recency_level]
    frequency = LEVEL_SCORE[frequency_level]
    monetary = LEVEL_SCORE[monetary_level]

    # High-value customers
    if frequency >= 2 and monetary >= 2:
        if recency >= 1:
            return "Risk Altındaki Yüksek Değerli Müşteriler"
        return "Yüksek Değerli Aktif Müşteriler"

    # Low-value customers
    if frequency <= -2 and monetary <= -2:
        if recency >= 1:
            return "Pasif Düşük Değerli Müşteriler"
        return "Aktif Düşük Değerli Müşteriler"

    # Very inactive customers should be identified explicitly
    if recency >= 2:
        if monetary >= 2:
            return "Risk Altındaki Yüksek Harcamalı Müşteriler"
        elif monetary >= 0:
            return "Pasifleşmiş Orta Değerli Müşteriler"
        else:
            return "Pasif Düşük Değerli Müşteriler"

    # Recent customers
    if recency <= -1:
        if monetary >= 2:
            return "Yüksek Harcamalı Aktif Müşteriler"

        if frequency >= 1 and monetary >= 1:
            return "Gelişen Değerli Müşteriler"

        if monetary >= 0 and frequency <= 0:
            return "Yakın Dönem Harcama Odaklı Müşteriler"

        if frequency >= 1:
            return "Aktif Sık Alım Yapan Müşteriler"

    # Remaining spending/frequency imbalance
    if monetary > frequency:
        return "Harcama Odaklı Müşteriler"

    if frequency > monetary:
        return "Etkileşim Odaklı Müşteriler"

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