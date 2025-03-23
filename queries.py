import sqlite3


def execute_query(query, params=()):
    """Функція для виконання SQL-запиту та виводу результату"""
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


# Отримати всі завдання певного користувача
def get_tasks_by_user(user_id):
    query = "SELECT * FROM tasks WHERE user_id = ?"
    return execute_query(query, (user_id,))


# Вибрати завдання за певним статусом
def get_tasks_by_status(status_name):
    query = """
        SELECT * FROM tasks 
        WHERE status_id = (SELECT id FROM status WHERE name = ?)
    """
    return execute_query(query, (status_name,))


# Оновити статус конкретного завдання
def update_task_status(task_id, new_status):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) 
        WHERE id = ?
    """,
        (new_status, task_id),
    )
    conn.commit()
    conn.close()


# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    query = """
        SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)
    """
    return execute_query(query)


# Додати нове завдання для конкретного користувача
def add_task(title, description, status_name, user_id):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (?, ?, (SELECT id FROM status WHERE name = ?), ?)
    """,
        (title, description, status_name, user_id),
    )
    conn.commit()
    conn.close()


# Отримати всі завдання, які ще не завершено
def get_unfinished_tasks():
    query = """
        SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """
    return execute_query(query)


# Видалити конкретне завдання
def delete_task(task_id):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# Знайти користувачів з певною електронною поштою
def find_users_by_email(email_pattern):
    query = "SELECT * FROM users WHERE email LIKE ?"
    return execute_query(query, (email_pattern,))


# Оновити ім'я користувача
def update_user_name(user_id, new_name):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET fullname = ? WHERE id = ?", (new_name, user_id))
    conn.commit()
    conn.close()


# Отримати кількість завдань для кожного статусу
def get_task_count_by_status():
    query = """
        SELECT s.name, COUNT(t.id) 
        FROM status s 
        LEFT JOIN tasks t ON s.id = t.status_id 
        GROUP BY s.name
    """
    return execute_query(query)


# Отримати завдання, які призначені користувачам з певною доменною частиною пошти
def get_tasks_by_email_domain(domain):
    query = """
        SELECT t.* FROM tasks t
        JOIN users u ON t.user_id = u.id
        WHERE u.email LIKE ?
    """
    return execute_query(query, ("%" + domain,))


# Отримати список завдань, що не мають опису
def get_tasks_without_description():
    query = "SELECT * FROM tasks WHERE description IS NULL OR description = ''"
    return execute_query(query)


# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_with_in_progress_tasks():
    query = """
        SELECT u.fullname, t.title FROM users u
        JOIN tasks t ON u.id = t.user_id
        WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress')
    """
    return execute_query(query)


# Отримати користувачів та кількість їхніх завдань
def get_users_with_task_count():
    query = """
        SELECT u.fullname, COUNT(t.id) FROM users u
        LEFT JOIN tasks t ON u.id = t.user_id
        GROUP BY u.fullname
    """
    return execute_query(query)


# 🔥 Тестуємо деякі функції:
if __name__ == "__main__":
    print("Завдання користувача з id=1:", get_tasks_by_user(1))
    print("Завдання зі статусом 'new':", get_tasks_by_status("new"))
    print("Користувачі без завдань:", get_users_without_tasks())
    print("Кількість завдань за статусами:", get_task_count_by_status())
    print(
        "Користувачі та їхні завдання 'in progress':",
        get_users_with_in_progress_tasks(),
    )
