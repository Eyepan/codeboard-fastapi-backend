import pandas as pd
from fastapi import FastAPI, Request
import sqlite3
from leetcode import get_leetcode_contest, get_leetcode_user
import nest_asyncio
nest_asyncio.apply()

app = FastAPI()
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


@app.on_event("startup")
def startup():
    # get_leetcode('weekly-contest-300')
    pass


@app.get("/leetcode/contest/{contest_code}")
def index(contest_code: str):
    return get_leetcode_contest(contest_code)


@app.get("/leetcode/user/{username}")
def get_user(username: str):
    return get_leetcode_user(username)
