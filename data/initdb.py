import json
import sqlite3
from pathlib import Path


def load_json_to_sqlite(json_path: str, db_path: str = "app.db"):
    # 1. Загрузка JSON
    with open(json_path, "r", encoding="utf-8") as f:
        texts = json.load(f)["texts"]

    # 2. Подключение к SQLite (если БД нет — она создастся)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 3. Создание таблицы (если её нет)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY,
            language TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            length INTEGER NOT NULL,
            content TEXT NOT NULL
        )
    """
    )

    # 4. Вставка данных
    for text in texts:
        cursor.execute(
            """
            INSERT INTO texts (id, language, difficulty, length, content)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                text["id"],
                text["language"],
                text["difficulty"],
                text["length"],
                text["content"],
            ),
        )

    # 5. Сохранение и закрытие
    conn.commit()
    conn.close()

    # Пример вызова
    # load_json_to_sqlite("data/texts.json", r"C:\Users\User\Desktop\sqlite\data.db")

# with open("data/words.json", "r", encoding="utf-8") as f:
#     words = json.load(f)["languages"]

conn = sqlite3.connect(r"C:\Users\User\Desktop\sqlite\data.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    language TEXT NOT NULL,
    word TEXT NOT NULL
);

"""
)
cursor.execute("CREATE INDEX IF NOT EXISTS idx_language ON words(language);")

cursor.execute('''
INSERT INTO words (language, word)
SELECT language, word 
FROM w
ORDER BY language, word  -- Сортировка по цене (убывание) и имени (возрастание)
''')

# for lang, word_list in words.items():
#     for word in word_list:
#         cursor.execute(
#             "INSERT INTO words (word, language) VALUES (?, ?)",
#             (word, lang)
#         )


conn.commit()
conn.close()
