from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import students_db, init_students_db
from src.routes.routes_students import router as students_router
from src.routes.routes_leetcode import router as leetcode_router
from src.routes.routes_codechef import router as codechef_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://codeboard-lac.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(students_router)
app.include_router(leetcode_router)
app.include_router(codechef_router)


@app.on_event("startup")
async def startup():
    init_students_db()


@app.get("/")
async def get_index():
    return "hello there"
