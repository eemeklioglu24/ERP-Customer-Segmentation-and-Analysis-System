import random
import pandas as pd
from datetime import datetime, timedelta
from .base import ERPInterface
from __future__ import annotations

import numpy as np
import pandas as p
import src.data_handler as data_handler

class FakeERP(ERPInterface):

    def __init__(self, num_customers = 100):
        self.num_customers = num_customers

    def get_customers(self):
        # Generates fake customers
        customers = []
        for i in range(self.num_customers):
            customers.append({
                "customer_id": f"C{i:04d}",
                "customer_name": f"Customer {i}"
            })
        return pd.DataFrame(customers)

    def get_sales(
        n_customers: int = 1000,
        n_products: int = 250,
        start_date: str = "2024-01-01",
        end_date: str = "2026-09-29",
        seed: int = 42,
    ) -> pd.DataFrame:

        rng = np.random.default_rng(seed)

        start = pd.Timestamp(start_date)
        end = pd.Timestamp(end_date)

        rows = []

        invoice_counter = 1
        stock_line_counter = 1

        for customer_number in range(1, n_customers + 1):

            customer_id = f"CUST_{customer_number:05d}"

            # For now: every customer has between 1 and 12 invoices
            n_invoices = rng.integers(1, 13)

            for _ in range(n_invoices):

                invoice_id = f"INV_{invoice_counter:07d}"
                invoice_counter += 1

                # Random invoice date inside the selected date range
                date_range_days = (end - start).days

                invoice_date = start + pd.Timedelta(
                    days=int(rng.integers(0, date_range_days + 1))
                )

                # Every invoice contains between 1 and 6 stock lines
                n_lines = rng.integers(1, 7)

                invoice_lines = []

                for _ in range(n_lines):

                    stock_line_id = f"LINE_{stock_line_counter:09d}"
                    stock_line_counter += 1

                    product_number = rng.integers(1, n_products + 1)
                    product_id = f"PROD_{product_number:04d}"

                    quantity = int(rng.integers(1, 11))

                    unit_price = round(float(rng.uniform(20, 2000)), 2,)

                    line_total = round(quantity * unit_price, 2,)

                    invoice_lines.append(
                        {
                            "stock_line_id": stock_line_id,
                            "product_id": product_id,
                            "quantity": quantity,
                            "line_total": line_total,
                        }
                    )

                # Equivalent idea to I.NETTOTAL for our simple first version
                invoice_amount = round(sum(line["line_total"] for line in invoice_lines), 2,)

                # Flatten invoice + its stock lines just like the SQL JOIN
                for line in invoice_lines:

                    rows.append(
                        {
                            "customer_id": customer_id,
                            "invoice_id": invoice_id,
                            "invoice_date": invoice_date,
                            "amount": invoice_amount,
                            "stock_line_id": line["stock_line_id"],
                            "product_id": line["product_id"],
                            "quantity": line["quantity"],
                            "line_total": line["line_total"],
                        }
                    )

        df = pd.DataFrame(rows)

        return df

    def refresh_features(self):
        sales = self.get_sales()
        features = data_handler.calculate_customer_features(sales)
        data_handler.dataframe_to_csv(features, "docs/Customer Features.csv")
        return features