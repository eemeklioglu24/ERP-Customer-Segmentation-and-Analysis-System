from src.erp.db_connection import create_connection

def get_available_tables(config: dict):
    conn = create_connection(config)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                TABLE_SCHEMA,
                TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME;
            """
        )
        rows = cursor.fetchall()
        tables = [{
            "schema": row.TABLE_SCHEMA,
            "table": row.TABLE_NAME
        } for row in rows]
        return tables
    finally:
        conn.close()
