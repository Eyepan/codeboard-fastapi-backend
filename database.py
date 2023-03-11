import sqlite3


def connection():
    return sqlite3.connect('db.sqlite3')
