import sqlite3
import traceback


def add_user_to_base(user: list):
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users_base(username, name) VALUES(?, ?);", user)
        conn.commit()
        return True
    except:
        print(user)
        print(traceback.format_exc())
        return False


def get_usernames():
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        usernames = cur.execute(f"SELECT username FROM users_base").fetchall()
        return list(map(lambda x: x[0], usernames))
    except:
        print(traceback.format_exc())
        return None


def get_name(username):
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        name = cur.execute(f"SELECT name FROM users_base WHERE username='{username}'").fetchall()[0]
        return name
    except:
        print(traceback.format_exc())
        return None

