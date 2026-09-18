import streamlit as st

from src.erp.db_connection import test_connection

def database_setup():
    st.subheader("Database Connection")

    if st.session_state.get("db_connected", False):
        st.success("Database connection established.")
        return st.session_state["db_config"]

    with st.form("database_connection_form"):
        server = st.text_input("Server")
        database = st.text_input("Database")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Test Connection")

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