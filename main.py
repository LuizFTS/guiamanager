from infrastructure.db.database import Database
from infrastructure.db.migrations import CREATE_TABLES_SCRIPT

def setup_database():
    db = Database()
    print(CREATE_TABLES_SCRIPT)
    db.execute_script(CREATE_TABLES_SCRIPT)

    print("Banco de dados criado e pronto para uso!")

def test_connection():
    db = Database()
    with db.connect() as conn:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Tabelas existentes:", rows)

if __name__ == "__main__":
    setup_database()
    test_connection()