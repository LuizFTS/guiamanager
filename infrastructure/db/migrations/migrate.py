import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "app_database.db"
MIGRATIONS_DIR = Path(__file__).parent

def get_conn():
    import os
    os.makedirs(DB_PATH.parent, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def ensure_migrations_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Schema_Migrations (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Filename" TEXT UNIQUE NOT NULL,
            "Applied_At" DATETIME DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

def applied_migrations(conn):
    cur = conn.cursor()
    # Tenta criar a tabela caso não exista
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Schema_Migrations (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Filename" TEXT UNIQUE NOT NULL,
            "Applied_At" DATETIME DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

    # Agora pega as migrations aplicadas
    cur.execute("SELECT Filename FROM Schema_Migrations")
    rows = cur.fetchall()
    return {row[0] for row in rows}  # garante que é um set de strings

def apply_migration(conn, path: Path):
    sql = path.read_text(encoding="utf-8-sig")
    cur = conn.cursor()
    try:
        cur.executescript(sql)
        cur.execute("INSERT INTO Schema_Migrations (Filename) VALUES (?)", (path.name,))
        conn.commit()
        print(f"[OK] Applied {path.name}")
    except Exception as e:
        conn.rollback()
        raise e

def main():
    print(DB_PATH)
    print(MIGRATIONS_DIR)
    conn = get_conn()

    cur = conn.cursor()

    cur.executescript("DELETE FROM schema_migrations WHERE filename='002_create_certificados.sql';")
    cur.executescript("DROP TABLE IF EXISTS Certificados;")
    cur.executescript("DROP TABLE IF EXISTS schema_migrations;")

    ensure_migrations_table(conn)
    applied = applied_migrations(conn)

    sql_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    for f in sql_files:
        print(f"Checking migration: {f.name}, applied set: {applied}, type of f.name: {type(f.name)}")
        if f.name not in applied:
            print(f"[APPLY] {f.name}")
            apply_migration(conn, f)
        else:
            print(f"[SKIP] {f.name}")

    conn.close()
    print("Migrations complete.")

if __name__ == "__main__":
    main()
