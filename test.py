import sqlite3
from pathlib import Path

DB_PATH = Path("C:/Users/lu9887091/OneDrive - Nutrien/Área de Trabalho/projects/GuiaManager/infrastructure/data/app_database.db")
SQL_PATH = Path("C:/Users/lu9887091/OneDrive - Nutrien/Área de Trabalho/projects/GuiaManager/infrastructure/db/migrations/002_create_certificados.sql")

print(DB_PATH)
print(SQL_PATH)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

sql = SQL_PATH.read_text(encoding="utf-8")
cur.executescript("")

cur.executescript(sql)
conn.commit()
conn.close()

print("Script executado com sucesso!")
