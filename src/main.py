from erp.fake_erp import FakeERP
import data_handler
import functions

from sklearn.preprocessing import StandardScaler
import matplotlib as plt

K = 4
plt.rcParams["axes3d.mouserotationstyle"] = "azel"

def main():

    # 1. Connect to data source
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

    # 7. Run clustering
    #labels = cluster_customers(X_scaled)
    data_handler.plot_X(X)
    memberships = functions.find_and_plot_clusters(X, N, K)
    functions.get_obj(X, N)

    # 8. Add cluster assignments back to the DataFrame
    rfm["cluster"] = memberships

    # 9. Show results
    data_handler.rfm_to_csv(rfm)


if __name__ == "__main__":
    main()