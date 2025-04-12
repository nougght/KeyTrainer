import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path):
        """
        :param db_path: Путь к существующему файлу БД
        """
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file {db_path} not found")

        # Проверяем целостность БД
        # self._check_connection()

    def _check_connection(self):
        """Проверяет, что файл БД валиден"""
        try:
            conn = self.get_connection()
            conn.execute("SELECT 1 FROM sqlite_master LIMIT 1")
            conn.close()
        except sqlite3.Error as e:
            raise ValueError(f"Invalid SQLite file: {e}")

    def get_connection(self) -> sqlite3.Connection:
        """Возвращает новое подключение к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
        return conn
