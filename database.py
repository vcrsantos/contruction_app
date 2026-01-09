import sqlite3

DB_NAME = "construcao.db"

def get_connection():
    """Establishes and returns a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initializes the database with the required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            casa_id INTEGER NOT NULL,
            FOREIGN KEY (casa_id) REFERENCES casas(id)
        )
    ''')
    
    conn.commit()
    conn.close()