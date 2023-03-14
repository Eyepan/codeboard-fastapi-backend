import sqlite3
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import math
from tqdm import tqdm
import json


def connection():
    return sqlite3.connect("leetcode.db")


def make_request(contest_code, page_num, pbar):
    url = f"https://leetcode.com/contest/api/ranking/{contest_code}/"
    params = {"pagination": page_num}
    response = requests.get(url, params=params)
    response.raise_for_status()
    pbar.update(1)
    return response.json()['total_rank']


def download_leetcode_contest_data(contest_code: str):
    print(f"Fetching data for {contest_code}")
    response = requests.get(
        f"https://leetcode.com/contest/api/ranking/{contest_code}/", params={"pagination": 1})
    response.raise_for_status()
    # write the response to a json file
    total_requests_to_make = math.ceil(
        response.json()['user_num'] / len(response.json()['total_rank']))
    total_data = []
    print(
        f"Getting {total_requests_to_make} pages of data for {contest_code} with {response.json()['user_num']} participants")
    with tqdm(total=total_requests_to_make) as pbar:
        with ThreadPoolExecutor() as executor:
            results = executor.map(make_request, [contest_code] * total_requests_to_make, range(
                1, total_requests_to_make + 1), [pbar] * total_requests_to_make)
            for result in results:
                total_data.extend(result)
    if not total_data:
        print("No data found for " + contest_code)
        return pd.DataFrame()
    df = pd.DataFrame(total_data)[['username', 'rank', 'score', 'finish_time']]
    return df


def get_leetcode_contest_ratings(contest_code: str):
    conn = connection()
    try:
        leetcode_contest_results = pd.read_sql(
            f'select * from "leetcode-{contest_code}"', con=conn)
    except:
        leetcode_contest_results = download_leetcode_contest_data(contest_code)
        leetcode_contest_results.to_sql(
            f'leetcode-{contest_code}', con=conn, if_exists='replace', index=False)
    return leetcode_contest_results.to_dict('records')


if __name__ == '__main__':
    try:
        for i in range(268, 336):
            print(
                f'CONTEST: WEEKLY-CONTEST-{i}', get_leetcode_contest_ratings(f'weekly-contest-{i}')[0])
    except Exception as e:
        print("Api failed here lol")
        print(str(e))
    try:
        for i in range(60, 99):
            print(
                f'CONTEST: biweekly-contest-{i}', get_leetcode_contest_ratings(f'biweekly-contest-{i}')[0])
    except Exception as e:
        print("Api failed here lol")
        print(str(e))
