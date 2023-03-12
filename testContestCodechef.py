import os
import requests
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/{comp}")
async def rankings_bouncer(comp: str):
    x = requests.get(
        f"https://www.codechef.com/api/rankings/{comp}?sortBy=rank&order=asc&page=1&itemsPerPage=25").json()
    return {"result": x}


@app.get("/autocomplete/{comp}/{my_filter}")
async def autocomplete(comp: str, my_filter: str):
    x = requests.get(
        f"https://www.codechef.com/api/rankings/{comp}/autocomplete/?qparam=institution&institution={my_filter}").json()
    return {"result": x}


@app.get("/")
async def hello_world():
    return "Hello, world! <a href='https://github.com/rhnvrm/codechef-api-bouncer'>Fork me on GitHub!</a>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
