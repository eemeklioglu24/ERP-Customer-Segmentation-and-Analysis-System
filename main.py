from src.erp.fake_erp import FakeERP
from src.erp.logo_erp import LogoERP
from src import data_handler, functions, interpreter

import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib as plt
import matplotlib.pyplot as pltplt


def run_pipeline(num_customers=200, K=3):

    # 1. Connect to data source
    plt.rcParams["axes3d.mouserotationstyle"] = "azel"
    # For syntethic data, use:
    # erp = FakeERP(num_customers=200)
    # For real data, use:
    erp = LogoERP()
    scaler = StandardScaler()

    # 2. Get raw ERP transactions
    sales = erp.get_sales()

    # 3. Convert transactions into RFM data
    # rfm = data_handler.calculate_rfm(sales)
    customer_features = data_handler.calculate_customer_features(sales)

    # 4. Keep customer IDs separately
    customer_ids = customer_features["customer_id"].to_numpy()
    N = customer_ids.size

    # 5. Convert customer features to an N x D NumPy array
    # X = data_handler.rfm_to_X(rfm, scaler)
    X = data_handler.features_to_X(customer_features, scaler)

    # 6. Run clustering
    data_handler.plot_X(X)
    memberships, centroids = functions.find_and_plot_clusters(X, N, K)
    objective_values = functions.get_obj(X, N)

    # 7. Add cluster assignments back to the DataFrame, and interpret the data
    customer_features["cluster"] = memberships
    normal_centroids = data_handler.inverse_centroids(centroids, scaler)
    cluster_data = pd.DataFrame({
        "cluster": range(len(centroids)),

        "recency_z": centroids[:, 0],
        "frequency_z": centroids[:, 1],
        "monetary_z": centroids[:, 2],

        "recency": normal_centroids[:, 0],
        "frequency": normal_centroids[:, 1],
        "monetary": normal_centroids[:, 2],
    })
    rfm_clustered = customer_features.copy()
    insight = interpreter.interpret(cluster_data, rfm_clustered)
    cluster_profile = (
        customer_features
        .groupby("cluster")
        .agg(
            customer_count=("customer_id", "count"),
            recency=("recency", "mean"),
            transaction_count=("transaction_count", "mean"),
            monetary=("monetary", "mean"),
            avg_order_value=("avg_order_value", "mean"),
            product_count=("product_count", "mean"),
            total_quantity=("total_quantity", "mean")
        )
    )

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

    return {
        "sales": sales,
        "features": customer_features,
        "X": X,
        "customer_ids": customer_ids,
        "memberships": memberships,
        "centroids": centroids,
        "objective_values": objective_values,
        "K": K,
        "cluster_insights": insight
    }

def main(K= 3):
    result = run_pipeline(K= 5)
    return result

if __name__ == "__main__":
    main()