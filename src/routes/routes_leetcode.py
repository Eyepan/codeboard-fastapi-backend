import json
import math
import queue
import threading

import pandas as pd
import requests
from fastapi import APIRouter, HTTPException
from tqdm import tqdm

from ..models.models_leetcode import StudentLeetCodeData, ContestResult
from ..database import connection

router = APIRouter(prefix='/api/leetcode')


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


@router.get("/contest/{contest_code}")
async def get_contest_details(contest_code: str) -> list[ContestResult]:
    conn = connection()
    try:
        df = pd.read_sql(f'select * from "leetcode-{contest_code}"', conn)
        conn.close()
        return json.loads(df.to_json(orient='records'))
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
        df = df[['username', 'rank', 'score']]
        df = df.sort_values(by='rank')
        df.to_sql(f'leetcode-{contest_code}', conn,
                  if_exists='replace', index=False)
        conn.close()
        return json.loads(df.to_json(orient='records'))


@router.get("/user/{username}")
async def get_user(username: str) -> StudentLeetCodeData:
    data = {
        "query": """
            query APIReq($username: String!) {
                allQuestionsCount {
                    difficulty
                    count
                }
                matchedUser(username: $username) {
                    username
                    profile {
                        ranking
                    }
                    problemsSolvedBeatsStats {
                        difficulty
                        percentage
                    }
                    submitStatsGlobal {
                        acSubmissionNum {
                            difficulty
                            count
                        }
                    }
                }
            }
            """,
        "variables": {"username": f"{username}"}
    }

    response = requests.post("https://leetcode.com/graphql/",
                             json=data)
    if 'errors' in response.text:
        raise HTTPException(
            404, f"Student {username} doesn't exist on leetcode")
    response.raise_for_status()
    return response.json()['data']
