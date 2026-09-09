from src.erp.fake_erp import FakeERP
from src import data_handler, functions
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib as plt


def run_pipeline(num_customers=200, k=3):

    # 1. Connect to data source
    K = 3
    plt.rcParams["axes3d.mouserotationstyle"] = "azel"
    erp = FakeERP(num_customers=200)

    # 2. Get raw ERP transactions
    sales = erp.get_sales()

    # 3. Convert transactions into RFM data
    rfm = data_handler.calculate_rfm(sales)

    # 4. Keep customer IDs separately
    customer_ids = rfm["customer_id"].to_numpy()
    N = customer_ids.size

    # 5. Convert RFM features to an N x D NumPy array
    X = data_handler.rfm_to_X(rfm)

    # 6. Run clustering
    data_handler.plot_X(X)
    memberships, centroids = functions.find_and_plot_clusters(X, N, K)
    objective_values = functions.get_obj(X, N)

    # 7. Add cluster assignments back to the DataFrame
    rfm["cluster"] = memberships

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
        "K": K
    }

def main():
    result = run_pipeline()
    return result

if __name__ == "__main__":
    main()