import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

from .base import ERPInterface
from src import data_handler
from src.erp import db_connection

class LogoERP(ERPInterface):
    # Retrieves data
    """
    Dimensions are:
    Recency,
    Monetary,
    Total Quantity,

    """
    def __init__(self, table_config= None):
        self.table_config = table_config

    def get_customers(self):
        return super().get_customers()

    def get_sales(self, conn, start_date, end_date):

        schema = self.quote_identifier(self.table_config["schema"])
        firm = self.table_config["firm"]
        periods = self.table_config["periods"]

        queries = []
        params = []
        for period in periods:

            invoice_table = self.quote_identifier(f"LG_{firm}_{period}_INVOICE")

            stockline_table = self.quote_identifier(f"LG_{firm}_{period}_STLINE")

            invoice_source = f"{schema}.{invoice_table}"
            stockline_source = f"{schema}.{stockline_table}"

            period_query = f"""
            SELECT
                I.CLIENTREF AS customer_id,
                I.LOGICALREF AS invoice_id,
                I.DATE_ AS invoice_date,
                I.NETTOTAL AS amount,

                L.LOGICALREF AS stock_line_id,
                L.STOCKREF AS product_id,
                L.AMOUNT AS quantity,
                L.TOTAL AS line_total
            FROM {invoice_source} AS I
            INNER JOIN {stockline_source} AS L
            ON L.INVOICEREF = I.LOGICALREF
            WHERE I.CANCELLED = 0
            AND L.LINETYPE = 0
            AND I.TRCODE = 8
            AND I.DATE_ >= ?
            AND I.DATE_ < ?
            """
            params.extend([
                start_date,
                end_date,
            ])

            queries.append(period_query)

        query = "\nUNION ALL\n".join(queries)

        sales = pd.read_sql_query(query, conn, params= params)

        # print(sales.shape)
        # print(sales["customer_id"].nunique())
        # print(sales.groupby("customer_id").size().describe())
        return sales

    def quote_identifier(self, identifier: str):
        return "[" + identifier.replace("]", "]]") + "]"
    
    def refresh_features(self, start_date, end_date, db_config= None):
        if db_config is None:
            raise ValueError("Database configuration not provided.")
        conn = db_connection.create_connection(db_config)
        try:
            sales = self.get_sales(conn, start_date, end_date)
            features = data_handler.calculate_customer_features(sales)
            data_handler.dataframe_to_csv(features, "docs/Customer Features.csv")
            return features
        finally:
            conn.close()

    def get_date_range(self, conn):

        schema = self.quote_identifier(self.table_config["schema"])
        firm = self.table_config["firm"]
        periods = self.table_config["periods"]

        queries = []

        for period in periods:
            invoice_table = self.quote_identifier(
                f"LG_{firm}_{period}_INVOICE"
            )

            invoice_source = f"{schema}.{invoice_table}"

            period_query = f"""
                SELECT
                    MIN(DATE_) AS min_date,
                    MAX(DATE_) AS max_date
                FROM {invoice_source}
            """

            queries.append(period_query)

        combined = "\nUNION ALL\n".join(queries)

        query = f"""
            SELECT
                MIN(min_date) AS min_date,
                MAX(max_date) AS max_date
            FROM (
                {combined}
            ) AS date_ranges
        """

        cursor = conn.cursor()
        cursor.execute(query)

        row = cursor.fetchone()

        return row[0], row[1]