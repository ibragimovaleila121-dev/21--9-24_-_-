import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "app.db")
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "database", "schema.sql")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    print("\n📂 Инициализация базы данных...")

    if not os.path.exists(SCHEMA_PATH):
        print(f"❌ Файл schema.sql не найден!")
        return False

    try:
        with get_connection() as conn:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        print("✅ База данных успешно создана!")
        return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка: {e}")
        return False