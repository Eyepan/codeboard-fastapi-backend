from models.models_leetcode import StudentLeetCodeData
from routes.routes_students import router as students_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes_leetcode import router as leetcode_router
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
app.include_router(leetcode_router)


@app.on_event("startup")
async def startup():
    initDB()
