import streamlit as st

from src.erp.db_connection import test_connection
from src.erp.db_metadata import get_available_tables

def database_setup():
    st.subheader("Veritabanı Bağlantısı")

    if st.session_state.get("db_connected", False):
        st.success("Veritabanı bağlantısı başarılı.")

        db_config = st.session_state["db_config"]

        if st.button("Bağlantı Değiştir"):
            st.session_state.pop("db_connected", None)
            st.session_state.pop("db_config", None)
            st.session_state.pop("tables_selected", None)
            st.session_state.pop("table_config", None)
            st.rerun()

        try:   
            tables = get_available_tables(db_config)
        except Exception as e:
            st.error(f"Veritabanı tablolarına erişim sağlanamadı: {e}")
            return None

        if not tables:
            st.warning("Erişilebilir tablo bulunamadı")
            return None

        return db_config

    with st.form("database_connection_form"):
        server = st.text_input("Server")
        database = st.text_input("Database")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Bağlantıyı Test Edin")

    if submitted:
        if not server or not database or not username or not password:
            st.warning("Please fill in all the database connection fields.")
            return None
        db_config = {
            "server": server,
            "database": database,
            "username": username,
            "password": password
        }

        try:
            test_connection(db_config)
        except Exception as e:
            st.session_state["db_connected"] = False
            st.error(f"Database connection failed: {e}")
            return None

        st.session_state["db_config"] = db_config
        st.session_state["db_connected"] = True
        st.rerun()
        return db_config
    return None