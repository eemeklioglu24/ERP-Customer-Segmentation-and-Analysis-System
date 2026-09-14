import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from openpyxl.styles import PatternFill

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

def calculate_customer_features(sales: pd.DataFrame, reference_date= None):
    # Calculates customer features with additional context regarding stock lines
    sales = sales.copy()
    sales["invoice_date"] = pd.to_datetime(sales['invoice_date'])

    # INVOICE LEVEL DATA
    invoices = (sales[
        [
                "invoice_id",
                "customer_id",
                "invoice_date",
                "amount"
            ]
        ].drop_duplicates(subset="invoice_id")
    )
    if (reference_date == None):
                reference_date = invoices["invoice_date"].max() + pd.Timedelta(days=1)
    else:
        reference_date = pd.to_datetime(reference_date)

    invoice_features = (
        invoices
        .groupby("customer_id")
        .agg(
            transaction_count=("invoice_id", "nunique"),
            monetary=("amount", "sum"),
            avg_order_value=("amount", "mean"),
            last_purchase=("invoice_date", "max")
        )
        .reset_index()
    )

    invoice_features["recency"] = (
        reference_date - invoice_features["last_purchase"]
    ).dt.days

    # STOCK LEVEL DATA
    stock_features = (
        sales
        .groupby("customer_id")
        .agg(
            product_count=("product_id", "nunique"),
            total_quantity=("quantity", "sum")
        )
        .reset_index()
    )

    # COMBINATION

    customer_features = invoice_features.merge(
        stock_features,
        on="customer_id",
        how="left"
    )

    customer_features = customer_features.drop(
        columns=["last_purchase"]
    )

    return customer_features


def rfm_to_X(rfm: pd.DataFrame, scaler: StandardScaler):
    # Turns the RFM dataframe to a numpy array object and standardizes the data
    X = rfm[["recency", "frequency", "monetary"]].to_numpy()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def features_to_X(customer_features: pd.DataFrame, scaler: StandardScaler):
    # Turns the customer dataframe to a numpy array object and standardizes the data
    X = customer_features[["recency", "transaction_count", "monetary", "avg_order_value", "product_count", "total_quantity"]].to_numpy()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def inverse_centroids(centroids, scaler: StandardScaler):
    return scaler.inverse_transform(centroids)

def plot_X(X):
    # Plots X to visualize
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')
    ax.plot(X[:, 0], X[:, 1], X[:, 2], ".", markersize=10)
    ax.set_xlabel('Son Alışverişten Geçen Süre')
    ax.set_ylabel('İşlem Sayısı')
    ax.set_zlabel('Parasal Değer')
    ax.set_title("Müşteriler")
    plt.show()

def dataframe_to_csv(rfm: pd.DataFrame, name):
    # Saves rfm dataframe to an csv file
    rfm.to_csv(name, index=False)

def dataframe_to_excel(rfm: pd.DataFrame):
    import pandas as pd
    # Create a writer object
    with pd.ExcelWriter("./docs/Customer Stats.xlsx", engine='openpyxl') as writer:
        rfm.to_excel(writer, sheet_name='Sheet1', index=False)
        
        # Get the openpyxl objects
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # 1. Auto-fit column sizes to prevent clipping
        for col in worksheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)
            
        # 2. Add colors to the header row
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        for cell in worksheet[1]:  # Row 1 is the header
            cell.fill = header_fill
