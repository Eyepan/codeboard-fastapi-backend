from models.models_leetcode import StudentLeetCodeData
from routes_students import router as students_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from leetcode import get_leetcode_contest, get_leetcode_user
from database import initDB

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students_router)


@app.on_event("startup")
async def startup():
    initDB()


@app.get("/api/leetcode/contest/{contest_code}")
async def index(contest_code: str):
    return get_leetcode_contest(contest_code)


@app.get("/api/leetcode/user/{username}")
async def get_user(username: str):
    data = get_leetcode_user(username)
    # write to file
    with open("content.json", 'w') as f:
        f.write(data.__str__())
    return data
