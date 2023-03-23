import time
import threading
import schedule
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_students_db
from src.routes.routes_students import router as students_router
from src.routes.routes_students import load_leetcode_data
from src.routes.routes_leetcode import router as leetcode_router
from src.routes.routes_codechef import router as codechef_router

app = FastAPI()


app.include_router(students_router)
app.include_router(leetcode_router)
app.include_router(codechef_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://codeboard-lac.vercel.app",
                   "https://www.codeboard-lac.vercel.app", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Cors middleware applied")


def load_leetcode_data_in_background():
    load_leetcode_data()


schedule.every().day.at("00:00").do(load_leetcode_data_in_background)


def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=schedule_loop)
schedule_thread.start()


@app.on_event("startup")
def init():
    init_students_db()
    load_leetcode_data()


@app.get("/")
async def get_index():
    return "hello there"


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', reload=True)
