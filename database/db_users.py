import sqlite3

def init_db():
    with sqlite3.connect("quiz.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                fullname TEXT,
                total_correct INTEGER DEFAULT 0,
                total_wrong INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def add_user(user_id, username, fullname):
    with sqlite3.connect("quiz.db") as conn:
        conn.execute("INSERT OR IGNORE INTO users (user_id, username, fullname) VALUES (?, ?, ?)", (user_id, username or "Anonymous", fullname))
        conn.commit()

def update_score(user_id, is_correct):
    with sqlite3.connect("quiz.db") as conn:
        if is_correct:
            conn.execute("UPDATE users SET total_correct = total_correct + 1 WHERE user_id = ?", (user_id,))
        else:
            conn.execute("UPDATE users SET total_wrong = total_wrong + 1 WHERE user_id = ?", (user_id,))
        conn.commit()

def get_all_users():
    with sqlite3.connect("quiz.db") as conn:
        return conn.execute("SELECT user_id, username, fullname, total_correct, total_wrong FROM users").fetchall()

def clear_users():
    with sqlite3.connect("quiz.db") as conn:
        conn.execute("DELETE FROM users")
        conn.commit()
