import random
import pandas as pd
from datetime import datetime, timedelta
from .base import ERPInterface

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

    def get_sales(self):
        # Generates random sales data for fake customers
        sales = []

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2026, 9, 1)

        number_of_days = (end_date - start_date).days
        invoice_counter = 1
        for i in range(1, self.num_customers + 1):

            customer_id: f"C{i:04d}"
            number_of_orders = random.randint(1, 30)
            for j in range(number_of_orders):
                invoice_date = start_date + timedelta(days= random.randint(0, number_of_days))
                amount = round(random.uniform(100, 20000), 2)
                sales.append({
                    "customer_id": customer_id,
                    "invoice_id": invoice_counter,
                    "invoice_date": invoice_date,
                    "amount": amount
                })
                invoice_counter += 1
        return pd.DataFrame(sales)
            






    