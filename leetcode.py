import json
import requests
import math
from database import connection
import threading
import pandas as pd
import queue
from tqdm import tqdm
import sys


def make_request(contest_code, i, pbar, results_queue):

    url = f"https://leetcode.com/contest/api/ranking/{contest_code}/"
    params = {
        "pagination": i + 1,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()['total_rank']
    results_queue.put(data)
    pbar.update(1)


def get_leetcode_contest(contest_code: str):
    conn = connection()
    try:
        df = pd.read_sql(f'select * from "leetcode-{contest_code}"', conn)
        conn.close()
        return df.to_json()
    except:
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
        df.to_sql(f'leetcode-{contest_code}', conn,
                  if_exists='replace', index=False)
        conn.close()
        return df.to_json()


def get_leetcode_user(username: str):
    url = f'https://leetcode-stats-api.herokuapp.com/{username}/'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    if sys.argv[1] == 'contest':
        print(get_leetcode_contest(sys.argv[2]))
    elif sys.argv[1] == 'user':
        print(get_leetcode_user(sys.argv[2]))
