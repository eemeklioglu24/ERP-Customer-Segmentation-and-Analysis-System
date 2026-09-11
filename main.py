from src.erp.fake_erp import FakeERP
from src.erp.logo_erp import LogoERP
from src import data_handler, functions, interpreter

import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib as plt


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
    print(sales.shape)
    print(sales["customer_id"].nunique())
    print(sales["customer_id"].value_counts().head(10))
    # 3. Convert transactions into RFM data
    rfm = data_handler.calculate_rfm(sales)

    # 4. Keep customer IDs separately
    customer_ids = rfm["customer_id"].to_numpy()
    N = customer_ids.size

    # 5. Convert RFM features to an N x D NumPy array
    X = data_handler.rfm_to_X(rfm, scaler)

    # 6. Run clustering
    data_handler.plot_X(X)
    memberships, centroids = functions.find_and_plot_clusters(X, N, K)
    objective_values = functions.get_obj(X, N)

    # 7. Add cluster assignments back to the DataFrame, and interpret the data
    rfm["cluster"] = memberships
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
    rfm_clustered = rfm.copy()
    insight = interpreter.interpret(cluster_data, rfm_clustered)

    # 8. Save results
    data_handler.dataframe_to_csv(rfm, "./docs/Customer Data.csv")
    #data_handler.dataframe_to_excel(rfm, "./docs/Customer Stats.xlsx")

    # 9. Return Data
    return {
        "sales": sales,
        "rfm": rfm,
        "X": X,
        "customer_ids": customer_ids,
        "memberships": memberships,
        "centroids": centroids,
        "objective_values": objective_values,
        "K": K,
        "cluster_insights": insight
    }

def main(K= 3):
    result = run_pipeline(K= K)
    return result

if __name__ == "__main__":
    main()