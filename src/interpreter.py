import pandas as pd

def classify_z(value):
    if value < -0.5:
        return "düşük"
    elif value > 0.5:
        return "yüksek"
    else:
        return "orta"

def classify_recency_z(value):
    if value < -0.5:
        return "yakın tarihli"
    elif value > 0.5:
        return "pasif"
    else:
        return "nispeten yakın tarihli"

def interpret_cluster(row):
    return{
        "cluster": int(row["cluster"]),
        "recency_level": classify_recency_z(row["recency_z"]),
        "frequency_level": classify_z(row["frequency_z"]),
        "monetary_level": classify_z(row["monetary_z"]),
        "recency": row["recency"],
        "frequency": row["frequency"],
        "monetary": row["monetary"]
    }

def interpret(cluster_data: pd.DataFrame):
    interpretations = []

    for _, row in cluster_data.iterrows():
        interpretations.append(
            interpret_cluster(row)
        )

    return interpretations


