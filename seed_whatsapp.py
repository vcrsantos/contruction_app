import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "construction.db")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

house = cursor.execute("SELECT id FROM houses WHERE name = 'Casa 2'").fetchone()
if not house:
    print("Casa 2 não encontrada!")
    conn.close()
    exit()

house_id = house[0]

expenses = [
    (17082.9, "Material", "2025-10-24", "Blocok"),
    (240, "Container", "2025-10-27", "Caçamba"),
    (200, "Container", "2025-10-27", ""),
    (1064, "Material", "2025-10-27", "Blocok"),
    (66, "Material", "2025-10-29", ""),
    (1920, "Material", "2025-11-03", ""),
    (2000, "Material", "2025-11-05", ""),
    (740, "Material", "2025-11-05", ""),
    (1589.5, "Material", "2025-11-06", "Cimento"),
    (4000, "Pedreiro", "2025-11-07", ""),
    (106, "Material", "2025-11-08", ""),
    (330, "Material", "2025-11-08", ""),
    (1220, "Material", "2025-11-10", ""),
    (60, "Engenheiro", "2025-11-12", ""),
    (470, "Material", "2025-11-13", ""),
    (1150, "Poste", "2025-11-13", ""),
    (251.92, "Material", "2025-11-14", "Vedacit Mercado Livre"),
    (8541.45, "Material", "2025-11-17", ""),
    (1850, "Material", "2025-11-18", "Ferragens"),
    (45, "Engenheiro", "2025-11-18", ""),
    (1030, "Engenheiro", "2025-11-18", ""),
    (923.7, "Material", "2025-11-21", ""),
    (3000, "Pedreiro", "2025-11-21", ""),
    (750, "Material", "2025-11-25", ""),
    (44, "Material", "2025-11-25", ""),
    (8541.45, "Material", "2025-11-25", ""),
    (10, "Engenheiro", "2025-11-26", ""),
    (940, "Material", "2025-11-27", ""),
    (245.04, "Material", "2025-11-28", "Aluguel de ferramentas"),
    (37, "Engenheiro", "2025-11-28", ""),
    (3000, "Pedreiro", "2025-12-05", ""),
    (1385.55, "Material", "2025-12-05", ""),
    (37, "Engenheiro", "2025-12-05", ""),
    (470, "Material", "2025-12-05", "Areia"),
    (80, "Consumo Luz", "2025-12-15", ""),
    (490, "Material", "2025-12-16", ""),
    (4100, "Material", "2025-12-16", "Laje"),
    (3000, "Pedreiro", "2025-12-19", ""),
    (600, "Material", "2026-01-06", ""),
    (50, "Material", "2026-01-06", ""),
    (945, "Escritório", "2026-01-07", ""),
    (945, "Escritório", "2026-01-07", ""),
    (630, "Escritório", "2026-01-07", ""),
    (449, "Material", "2026-01-08", ""),
    (290, "Material", "2026-01-08", ""),
    (2000, "Pedreiro", "2026-01-09", ""),
    (375, "Material", "2026-01-17", ""),
    (60, "Material", "2026-01-17", ""),
    (482, "Material", "2026-01-17", ""),
    (20, "Material", "2026-01-20", ""),
    (150, "Material", "2026-01-22", ""),
    (59, "Material", "2026-01-22", ""),
    (4120, "Material", "2026-01-22", "Concreto"),
    (2000, "Pedreiro", "2026-01-23", ""),
    (30, "Material", "2026-01-23", ""),
    (470, "Material", "2026-01-26", ""),
    (1358.5, "Material", "2026-01-30", ""),
    (1000, "Pedreiro", "2026-01-30", ""),
    (1300, "Material", "2026-01-30", ""),
    (245.52, "Material", "2026-02-02", ""),
    (695, "Escritório", "2026-02-02", ""),
    (1000, "Pedreiro", "2026-02-06", ""),
    (30, "Material", "2026-02-09", ""),
    (3700, "Material", "2026-02-10", "Portão"),
    (290, "Material", "2026-02-10", "Aluguel de ferramentas"),
    (379.9, "Material", "2026-02-10", "Caixa d'água"),
    (646.13, "Material", "2026-02-18", ""),
    (200, "Material", "2026-02-19", ""),
    (107.07, "Consumo Luz", "2026-02-20", ""),
    (2000, "Pedreiro", "2026-02-20", ""),
    (37, "Material", "2026-02-20", ""),
    (3900, "Material", "2026-02-20", "Telhado"),
    (94, "Material", "2026-02-25", ""),
    (110, "Material", "2026-02-26", ""),
    (470, "Material", "2026-02-26", ""),
    (1750, "Material", "2026-02-27", ""),
    (240, "Container", "2026-02-28", ""),
    (2000, "Pedreiro", "2026-02-28", ""),
    (273, "Material", "2026-02-28", ""),
    (695, "Escritório", "2026-03-02", ""),
    (26.9, "Engenheiro", "2026-03-05", ""),
    (260, "Material", "2026-03-06", ""),
    (38, "Engenheiro", "2026-03-09", ""),
    (342, "Material", "2026-03-09", "Espuma Expansiva"),
    (303, "Consumo Água", "2026-03-13", ""),
]

for value, category, date, obs in expenses:
    cursor.execute(
        "INSERT INTO expenses (value, category, date, house_id, observations) VALUES (?, ?, ?, ?, ?)",
        (value, category, date, house_id, obs),
    )

conn.commit()
conn.close()
print(f"{len(expenses)} gastos inseridos para Casa 2.")
