import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "construction.db")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Replace old categories with new ones
cursor.execute("DELETE FROM categories")
new_categories = [
    'Terreno', 'Cartório', 'Desmembramento', 'Limpeza terreno',
    'Engenheiro', 'Container', 'Poste', 'Material', 'Pedreiro',
    'Escritório', 'IPTU', 'Alvara', 'Consumo Água', 'Consumo Luz',
    'Eletricista', 'Imposto', 'Seguro',
]
for name in new_categories:
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

# Get Casa 2 ID
house = cursor.execute("SELECT id FROM houses WHERE name = 'Casa 2'").fetchone()
if not house:
    print("Casa 2 não encontrada!")
    conn.close()
    exit()

house_id = house[0]

expenses = [
    (8500.00,  "Terreno",    "2024-03-27", ""),
    (1562.79,  "Cartório",   "2024-03-27", ""),
    (261.00,   "Cartório",   "2024-03-19", ""),
    (25000.00, "Cartório",   "2024-03-27", ""),
    (734.06,   "Cartório",   "2024-04-09", ""),
    (750.00,   "Desmembramento", "2024-04-29", ""),
    (275.00,   "Limpeza terreno", "2024-04-29", ""),
    (112.91,   "Cartório",   "2024-07-23", ""),
    (140.00,   "Cartório",   "2024-07-30", ""),
    (90.34,    "Cartório",   "2024-08-01", ""),
    (750.00,   "Engenheiro", "2024-08-15", ""),
]

for value, category, date, obs in expenses:
    cursor.execute(
        "INSERT INTO expenses (value, category, date, house_id, observations) VALUES (?, ?, ?, ?, ?)",
        (value, category, date, house_id, obs),
    )

conn.commit()
conn.close()
print(f"Categorias atualizadas e {len(expenses)} gastos inseridos para Casa 2.")
