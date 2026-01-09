import sqlite3

DB_NAME = "construction.db"

def get_connection():
    """Establishes and returns a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initializes the database with the required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS houses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            house_id INTEGER NOT NULL,
            FOREIGN KEY (house_id) REFERENCES houses(id)
        )
    ''')
    
    conn.commit()
    conn.close()