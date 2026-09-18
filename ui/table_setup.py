import re
import streamlit as st

from src.erp.db_metadata import get_available_tables


def table_selection(db_config):

    st.subheader("Data Source Selection")

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

    selected_schema = st.selectbox(
        "Schema",
        schemas
    )

    schema_tables = [
        table["table"]
        for table in tables
        if table["schema"] == selected_schema
    ]

    pattern = re.compile(
        r"^LG_(\d+)_(\d+)_(INVOICE|STLINE)$",
        re.IGNORECASE
    )

    available_sources = {}

    for table_name in schema_tables:

        match = pattern.match(table_name)

        if not match:
            continue

        firm = match.group(1)
        period = match.group(2)
        table_type = match.group(3).upper()

        key = (firm, period)

        if key not in available_sources:
            available_sources[key] = {}

        available_sources[key][table_type] = table_name

    # IMPORTANT: this must be OUTSIDE the for-loop
    valid_sources = {
        key: value
        for key, value in available_sources.items()
        if "INVOICE" in value and "STLINE" in value
    }

    if not valid_sources:
        st.warning(
            "No valid Firm / Period combinations containing both "
            "INVOICE and STLINE tables were found."
        )
        return None

    firms = sorted(
        set(firm for firm, period in valid_sources.keys())
    )

    selected_firm = st.selectbox(
    "Firm",
    firms
    )

    periods = sorted(
        period
        for firm, period in valid_sources.keys()
        if firm == selected_firm
    )

    selected_period = st.selectbox(
        "Period",
        periods
    )

    source = valid_sources[
        (selected_firm, selected_period)
    ]

    st.write(
        "Invoice:",
        source["INVOICE"]
    )

    st.write(
        "Stock Line:",
        source["STLINE"]
    )

    submitted = st.button("Continue")

    if submitted:

        table_config = {
            "schema": selected_schema,
            "firm": selected_firm,
            "period": selected_period,
            "invoice_table": source["INVOICE"],
            "stockline_table": source["STLINE"],
        }

        st.session_state["table_config"] = table_config
        st.session_state["tables_selected"] = True

        st.rerun()

    return None