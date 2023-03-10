import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from leetcode import get_leetcode
import nest_asyncio
nest_asyncio.apply()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


@app.on_event("startup")
def startup():
    # get_leetcode('weekly-contest-300')
    pass


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    result = pd.read_csv('leetcode_weekly-contest-300.csv').to_html()
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
