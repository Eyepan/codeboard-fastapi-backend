from routes_students import router as students_router
from fastapi import FastAPI
from leetcode import get_leetcode_contest, get_leetcode_user
from database import initDB


app = FastAPI()

app.include_router(students_router)


@app.on_event("startup")
async def startup():
    initDB()


@app.get("/api/leetcode/contest/{contest_code}")
async def index(contest_code: str):
    return get_leetcode_contest(contest_code)


@app.get("/api/leetcode/user/{username}")
async def get_user(username: str):
    return get_leetcode_user(username)
