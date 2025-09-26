import sqlite3
from pathlib import Path
from shared.settings import DATABASE_PATH


class Database:
    """Gerencia a conexão SQLite com contexto seguro."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_file()

    def _ensure_file(self):
        # Cria pasta caso não exista
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        """Retorna uma conexão sqlite3 com foreign keys habilitadas."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def execute_script(self, script: str):
        """Executa scripts de criação ou migração."""
        with self.connect() as conn:
            conn.executescript(script)
            conn.commit()
