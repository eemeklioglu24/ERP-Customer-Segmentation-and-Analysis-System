import streamlit as st

from src.erp.db_metadata import get_available_tables


def table_selection(db_config):

    st.subheader("Veri Kaynağı Seçimi")

    # If tables were already selected, return them.
    if st.session_state.get("tables_selected", False):
        return st.session_state["table_config"]

    try:
        tables = get_available_tables(db_config)

    except Exception as e:
        st.error(f"Could not retrieve database tables: {e}")
        return None

    if not tables:
        st.warning("No accessible tables were found.")
        return None

    schemas = sorted(
        set(table["schema"] for table in tables)
    )

    with st.form("table_selection_form"):

        selected_schema = st.selectbox(
            "Şema",
            schemas
        )

        schema_tables = [
            table["table"]
            for table in tables
            if table["schema"] == selected_schema
        ]

        invoice_tables = [
            table
            for table in schema_tables
            if "INVOICE" in table.upper()
        ]

        stockline_tables = [
            table
            for table in schema_tables
            if "STLINE" in table.upper()
        ]

        selected_invoice_table = st.selectbox(
            "Fatura Tablosu",
            invoice_tables
        )

        selected_stockline_table = st.selectbox(
            "Stok Hattı Tablosu",
            stockline_tables
        )

        submitted = st.form_submit_button(
            "Devam Et"
        )

    if submitted:

        table_config = {
            "schema": selected_schema,
            "invoice_table": selected_invoice_table,
            "stockline_table": selected_stockline_table,
        }

        st.session_state["table_config"] = table_config
        st.session_state["tables_selected"] = True

        st.rerun()

    return None