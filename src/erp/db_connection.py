import pyodbc

def create_connection(config: dict):
    server = config["server"]
    database = config["database"]
    username = config["username"]
    password = config["password"]

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "TrustServerCertificate=yes"
    )

    return pyodbc.connect(connection_string, timeout=5)

def test_connection(config: dict):
    conn = None
    try:
        conn = create_connection(config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return True
    finally:
        if conn is not None:
            conn.close