import sqlite3
from faker import Faker
import random

db_name = "task_manager.db"
fake = Faker()

# Підключаємося до бази даних
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Створюємо таблиці
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""
)

# Додаємо статуси
statuses = [("new",), ("in progress",), ("completed",)]
cursor.executemany("INSERT OR IGNORE INTO status (name) VALUES (?)", statuses)

# Додаємо випадкових користувачів
users = [(fake.name(), fake.unique.email()) for _ in range(10)]
cursor.executemany("INSERT INTO users (fullname, email) VALUES (?, ?)", users)

# Отримуємо ID користувачів та статусів
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM status")
status_ids = [row[0] for row in cursor.fetchall()]

# Додаємо випадкові завдання
tasks = [
    (fake.sentence(), fake.text(), random.choice(status_ids), random.choice(user_ids))
    for _ in range(20)
]
cursor.executemany(
    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
    tasks,
)

# Збереження змін та закриття підключення
conn.commit()
conn.close()
print("База даних створена і заповнена успішно!")
