import sqlite3

conn = sqlite3.connect("chat_users.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    room TEXT NOT NULL,
    message TEXT NOT NULL
)''')

conn.commit()

def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

def save_message(username, room, message):
    c.execute("INSERT INTO history (username, room, message) VALUES (?, ?, ?)", (username, room, message))
    conn.commit()

def get_message_history(room):
    c.execute("SELECT username, message FROM history WHERE room=? ORDER BY id ASC", (room,))
    return c.fetchall()

def is_admin(username, password):
    return username == "admin" and password == "admin123"

def delete_user(username):
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    print(f"✅ Deleted user: {username}")

def delete_all_users():
    c.execute("DELETE FROM users")
    conn.commit()
    print("⚠️ All users deleted.")
