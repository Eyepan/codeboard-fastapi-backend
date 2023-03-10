import json
import requests
import math
import sqlite3
import threading
import pandas as pd
import queue
from tqdm import tqdm


def make_request(contest_code, i, pbar, results_queue):
    url = f"https://leetcode.com/contest/api/ranking/{contest_code}/"
    params = {
        "pagination": i + 1,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Response failed while requesting page {i + 1}")
        exit()
    data = response.json()['total_rank']
    results_queue.put(data)
    pbar.update(1)


def glc(contest_code: str):
    url = f"https://leetcode.com/contest/api/ranking/{contest_code}/"
    params = {
        "pagination": 1,
    }
    print(f"Fetching data for {contest_code}")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("something went wrong")
        exit()

    total_requests_to_make = math.ceil(
        response.json()['user_num'] / len(response.json()['total_rank']))

    total_ranks = []

    print(
        f"Getting {total_requests_to_make} pages of data for {contest_code} with {response.json()['user_num']} participants")

    with tqdm(total=total_requests_to_make) as pbar:
        results_queue = queue.Queue()
        threads = []
        for i in range(total_requests_to_make):
            thread = threading.Thread(target=make_request, args=(
                contest_code, i, pbar, results_queue))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        while not results_queue.empty():
            total_ranks.extend(results_queue.get())

    df = pd.read_json(json.dumps(total_ranks))

    df = df[['username', 'rank', 'score', 'finish_time']]
    df.to_sql(f'leetcode-{contest_code}', con=sqlite3.connect(
        "db.sqlite3"), if_exists="replace")
    df.to_csv(f"leetcode_{contest_code}.csv", index=False)
    print(f"Done for {contest_code}!")


def get_leetcode(contest_code: str):
    glc(contest_code)
