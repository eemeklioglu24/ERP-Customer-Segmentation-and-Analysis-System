import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def calculate_rfm(sales: pd.DataFrame, reference_date= None):
    # calculates Recency, Frequency, and Monetary from sales data. Does not care whether sales is synthesized or real
    sales = sales.copy()
    sales["invoice_date"] = pd.to_datetime(sales['invoice_date'])
    if reference_date is None:
        reference_date = sales["invoice_date"].max() + pd.Timedelta(days=1)

    rfm = sales.groupby("customer_id").agg(
        last_purchase= ("invoice_date", "max"),
        frequency= ("invoice_id", "nunique"),
        monetary= ("amount", "sum")
    ).reset_index()

    rfm["recency"] = (
        reference_date - rfm["last_purchase"]
    ).dt.days

    return rfm[
        [
            "customer_id",
            "recency",
            "frequency",
            "monetary"
        ]
    ]

def rfm_to_X(rfm: pd.DataFrame):
    X = rfm[["recency", "frequency", "monetary"]].to_numpy()
    scalar = StandardScaler()
    X_scaled = scalar.fit_transform(X)
    return X_scaled

def plot_X(X):
    # Plots X to visualize
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')
    ax.plot(X[:, 0], X[:, 1], X[:, 2], ".", markersize=10)
    ax.set_xlabel('Son Alışverişten Geçen Süre')
    ax.set_ylabel('Frekans')
    ax.set_zlabel('Parasal Değer')
    ax.set_title("Müşteriler")
    plt.show()