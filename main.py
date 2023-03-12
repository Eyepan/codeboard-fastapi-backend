from src.models.models_leetcode import StudentLeetCodeData
from src.routes.routes_students import router as students_router
from src.routes.routes_leetcode import router as leetcode_router
from src.routes.routes_codechef import router as codechef_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import initDB

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
app.include_router(codechef_router)


@app.on_event("startup")
async def startup():
    initDB()


@app.get("/")
async def hello():
    return "hi there"
