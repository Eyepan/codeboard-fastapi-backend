from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import sqlite3
import time
from turtle import pd

import requests
from tqdm import tqdm


def students_db():
    return sqlite3.connect("./databases/students.db")


def leetcode_db():
    return sqlite3.connect("./databases/leetcode.db")


def codechef_db():
    return sqlite3.connect("./databases/codechef.db")


def init_students_db():
    conn = students_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS students(
        id TEXT PRIMARY KEY NOT NULL, 
        name TEXT NOT NULL, 
        dept TEXT NOT NULL, 
        batch INTEGER NOT NULL, 
        leetcode_username TEXT NOT NULL, 
        codechef_username TEXT NOT NULL, 
        codeforces_username TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()
