import json
import queue
import threading

import pandas as pd
import requests
from fastapi import APIRouter
from tqdm import tqdm

from ..database import connection

router = APIRouter(prefix='/api/codechef')

headers = {
    'Cookie': 'SESS93b6022d778ee317bf48f7dbffe03173=74faa6408dc8cc6fd6f07ba3cfa584fe; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiIzNTQxNDQ1IiwidXNlcm5hbWUiOiJpYW10ZW9nZ3kiLCJpYXQiOjE2Nzg1ODgzNzAsIm5iZiI6MTY3ODU4ODM3MCwiZXhwIjoxNjgwNTgyNzcwfQ.lpv5CRXuuLqfTO5NoM7dNbT1S_UMyAdaPehpUig2t00; uid=3541445',
    'x-csrf-token': '76313213fb21041a17d3281f49b7be049a4cf6f127645eebe0bd7c393a035721',
}


def make_request(contest_code, i, headers, pbar, results_queue):
    url = f"https://www.codechef.com/api/rankings/{contest_code}"
    params = {
        "itemsPerPage": 100,
        "order": "asc",
        "page": i,
        "sortBy": "rank",
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()['list']
    results_queue.put(data)
    pbar.update(1)


@router.get("/contest/{contest_code}")
async def index(contest_code: str):
    conn = connection()
    try:
        df = pd.read_sql(f'select * from "codechef-{contest_code}"', conn)
        conn.close()
        return json.loads(df.to_json(orient='records'))
    except:
        print(f"Fetching data for {contest_code}")
        response = requests.get(
            url=f'https://www.codechef.com/api/rankings/{contest_code}?itemsPerPage=100&order=asc&page=1&sortBy=rank', headers=headers)
        if response.status_code != 200:
            print("something went wrong")
            exit()
        total_requests_to_make = response.json()['availablePages']
        print(
            f"Getting {total_requests_to_make} pages of data for {contest_code} with {response.json()['totalItems']} participants")

        total_data = []
        with tqdm(total=total_requests_to_make) as pbar:
            results_queue = queue.Queue()
            threads = []
            for i in range(1, total_requests_to_make + 1):
                thread = threading.Thread(target=make_request, args=(
                    contest_code, i, headers, pbar, results_queue))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            while not results_queue.empty():
                total_data.extend(results_queue.get())
        df = pd.read_json(json.dumps(total_data))
        df = df[['rank', 'user_handle', 'score', 'total_time']]
        df = df.sort_values(by='rank')
        df.to_sql(f'codechef-{contest_code}', conn,
                  if_exists='replace', index=False)
        conn.close()
        return json.loads(df.to_json(orient='records'))