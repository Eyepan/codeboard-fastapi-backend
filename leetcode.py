import json
import requests
import math
import sqlite3
import asyncio
import pandas as pd
import aiohttp
import sys
from tqdm import tqdm

contest_code = sys.argv[1]

url = f"https://leetcode.com/contest/api/ranking/{contest_code}/"
params = {
    "pagination": 1,
}


async def make_request(i, pbar):
    params = {
        "pagination": i + 1,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                print(f"Response failed while requesting page {i + 1}")
                return 0
            data = (await response.json())['total_rank']
            pbar.update(1)
            return data


async def main():
    print(f"Fetching data for {contest_code}")
    response = requests.get(url, params=params)

    if (response.status_code != 200):
        print("something went wrong")
        raise 'status code not 200'

    total_requests_to_make = math.ceil(
        response.json()['user_num'] / len(response.json()['total_rank']))

    num_threads = 4
    total_ranks = []

    print(
        f"Getting {total_requests_to_make} pages of data for {contest_code} with {response.json()['user_num']} participants")

    with tqdm(total=total_requests_to_make) as pbar:
        tasks = []
        for i in range(total_requests_to_make):
            tasks.append(asyncio.ensure_future(make_request(i, pbar)))

        results = await asyncio.gather(*tasks)

    total_ranks = sum(results, [])

    df = pd.read_json(json.dumps(total_ranks))

    # reduce to simpler columns
    df = df[['username', 'rank', 'score', 'finish_time']]
    df.to_sql(f'leetcode-{contest_code}', con=sqlite3.connect(
        "db.sqlite3"), if_exists="replace")

    print(f"Done for {contest_code}!")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
