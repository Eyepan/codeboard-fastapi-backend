import sqlite3


def connection():
    return sqlite3.connect('db.sqlite3')


def initDB():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS students(
        id TEXT PRIMARY KEY NOT NULL, 
        name TEXT NOT NULL, 
        dept TEXT NOT NULL, 
        batch INTEGER NOT NULL, 
        leetcode_username TEXT UNIQUE NOT NULL, 
        codechef_username TEXT UNIQUE NOT NULL, 
        codeforces_username TEXT UNIQUE NOT NULL
    )""")
    conn.commit()
    conn.close()


initDB()
