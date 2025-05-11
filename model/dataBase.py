import sqlite3
from pathlib import Path
from utils import resource_path

# модель базы данных
class Database:
    def __init__(self, db_path):
        self.db_path = Path(resource_path(db_path))
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file {db_path} not found")


    def _check_connection(self):
        try:
            conn = self.get_connection()
            conn.execute("SELECT 1 FROM sqlite_master LIMIT 1")
            conn.close()
        except sqlite3.Error as e:
            raise ValueError(f"Invalid SQLite file: {e}")

    # возвращает подключение к бд
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
        return conn
