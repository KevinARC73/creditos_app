import sqlite3

dbname = "creditos.db"

def get_connection():
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creditos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                monto REAL NOT NULL,
                tasa_interes REAL NOT NULL,
                plazo INTEGER NOT NULL,
                fecha_otorgamiento TEXT NOT NULL
            )
        """)
        conn.commit()
"""
if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM creditos")
    rows = cursor.fetchall()
    for row in rows:
        print(dict(row))  # Para ver cada registro como diccionario
"""