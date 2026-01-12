import sqlite3

DB_NAME = "construction.db"

CATEGORIES_DEFAULT = [
    'Aquisição e Regularização',
    'Preparação do Terreno',
    'Mão de Obra',
    'Materiais de Construção',
    'Projetos e Técnicos',
    'Infraestrutura da Obra',
    'Custos Administrativos',
]

def seed_categories():
    """Seeds the database with default categories if none exist."""
    conn = get_connection()
    cursor = conn.cursor()

    for category in CATEGORIES_DEFAULT:
        cursor.execute(
            "INSERT INTO categories (name) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = ?)",
            (category, category)
        )

    conn.commit()
    conn.close()

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
            name TEXT NOT NULL,
            selling_price REAL,
            observations TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            observations TEXT,
            house_id INTEGER NOT NULL,
            FOREIGN KEY (house_id) REFERENCES houses(id)
        )
    ''')
    
    conn.commit()
    conn.close()