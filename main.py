from src.erp.fake_erp import FakeERP
from src.erp.logo_erp import LogoERP
from src import data_handler, functions, interpreter

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib as plt
import matplotlib.pyplot as pltplt

def run_pipeline(num_customers=200, K=3, n_init= 5):

    # 1. Connect to data source
    plt.rcParams["axes3d.mouserotationstyle"] = "azel"
    scaler = StandardScaler()

    # 2. read Features
    customer_features = pd.read_csv(
        "./docs/Customer Features.csv"
    )

    # 4. Keep customer IDs separately
    customer_ids = customer_features["customer_id"].to_numpy()
    N = customer_ids.size

    # 5. Convert customer features to an N x D NumPy array
    # X = data_handler.rfm_to_X(rfm, scaler)
    X = data_handler.features_to_X(customer_features, scaler)

    # 6. Run clustering
    data_handler.plot_X(X)
    #memberships, centroids = functions.find_and_plot_clusters(X, N, K)
    objective_values, memberships, centroids, silhouette_scores = functions.robust_kmeans(X, N, K, n_init)
    # objective_values, silhouette_scores = functions.get_obj(X, N, n_init)

    # 7. Add cluster assignments back to the DataFrame, and interpret the data
    customer_features["cluster"] = memberships
    normal_centroids = data_handler.inverse_centroids(centroids, scaler)
    cluster_data = pd.DataFrame({
        "cluster": range(len(centroids)),

        "recency_z": centroids[:, 0],
        "frequency_z": centroids[:, 1],
        "monetary_z": centroids[:, 2],
        "avg_order_value_z": centroids[:, 3],
        "product_count_z": centroids[:, 4],
        "total_quantity_z": centroids[:, 5],

        "recency": normal_centroids[:, 0],
        "frequency": normal_centroids[:, 1],
        "monetary": normal_centroids[:, 2],
        "avg_order_value": normal_centroids[:, 3],
        "product_count": normal_centroids[:, 4],
        "total_quantity": normal_centroids[:, 5],
    })
    features_clustered = customer_features.copy()
    insight = interpreter.interpret(cluster_data, features_clustered)

    # 7.1. Add Principal Component Analysis for visualization
    X_pca = data_handler.get_X_pca(X)

    # print(cluster_profile)

    # 8. Save results
    data_handler.dataframe_to_csv(customer_features, "./docs/Customer Data.csv")
    #data_handler.dataframe_to_excel(rfm, "./docs/Customer Stats.xlsx")

    # 9. Return Data
    #print(customer_features.describe().to_string())
    feature_cols = ["recency", "monetary", "avg_order_value", "product_count", "transaction_count", "total_quantity"]
    print("\n///  CORRELATION     ///\n")
    print(customer_features[feature_cols].corr().to_string())

    print("\n///  CLUSTER COUNTS    ///\n")
    print(customer_features["cluster"].value_counts().sort_index())

    print("\n///  CLUSTER MEANS     ///\n")
    print(customer_features.groupby("cluster")[feature_cols].mean().round(2).to_string())

    # print("\n///  DIOGNOSTICS     ///\n")
    # diognostics = functions.diognose_k_values(X, N, 20)
    # print(diognostics.to_string())

    # unique, count = np.unique(memberships, return_counts=True)
    # print(dict(zip(unique, count)))

    # functions.diognose_specific_k(X, N, 2)

    return {
        "features": customer_features,
        "X": X,
        "X_pca": X_pca,
        "customer_ids": customer_ids,
        "memberships": memberships,
        "centroids": centroids,
        "objective_values": objective_values,
        "silhouette_scores": silhouette_scores,
        "K": K,
        "cluster_insights": insight
    }

def main(K= 3, n_init= 5):
    result = run_pipeline(K= K, n_init= n_init)
    return result

if __name__ == "__main__":
    main()