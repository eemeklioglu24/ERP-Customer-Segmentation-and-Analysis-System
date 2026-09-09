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

def rfm_to_X(rfm: pd.DataFrame):
    # Turns the RFM dataframe to a numpy array object and standardizes the data
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

def rfm_to_csv(rfm: pd.DataFrame):
    # Saves rfm dataframe to an csv file
    rfm.to_csv("./docs/Customer Data.csv", index=False)

def rfm_to_excel(rfm: pd.DataFrame):
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
