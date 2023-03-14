import sqlite3
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def connection():
    return sqlite3.connect('codechef.db')


def make_request(contest_code, page_num, headers, pbar):
    url = f"https://www.codechef.com/api/rankings/{contest_code}"
    params = {
        "itemsPerPage": 100,
        "order": "asc",
        "page": page_num,
        "sortBy": "rank",
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    pbar.update(1)
    return response.json()['list']


def download_codechef_contest_data(contest_code: str, division: str) -> pd.DataFrame:
    print(f"Fetching data for {contest_code}{division}")
    headers = {
        'Cookie': 'SESS93b6022d778ee317bf48f7dbffe03173=74faa6408dc8cc6fd6f07ba3cfa584fe; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiIzNTQxNDQ1IiwidXNlcm5hbWUiOiJpYW10ZW9nZ3kiLCJpYXQiOjE2Nzg1ODgzNzAsIm5iZiI6MTY3ODU4ODM3MCwiZXhwIjoxNjgwNTgyNzcwfQ.lpv5CRXuuLqfTO5NoM7dNbT1S_UMyAdaPehpUig2t00; uid=3541445',
        'x-csrf-token': '76313213fb21041a17d3281f49b7be049a4cf6f127645eebe0bd7c393a035721',
    }
    response = requests.get(
        url=f'https://www.codechef.com/api/rankings/{contest_code}{division}?itemsPerPage=100&order=asc&page=1&sortBy=rank', headers=headers)
    if response.status_code != 200:
        print(f"No data found for {contest_code}{division}")
        return pd.DataFrame()

    total_requests_to_make = response.json()['availablePages']
    total_data = []
    pbar = tqdm(total=total_requests_to_make)
    with ThreadPoolExecutor() as executor:
        results = executor.map(make_request, [f'{contest_code}{division}'] * total_requests_to_make, range(
            1, total_requests_to_make + 1), [headers] * total_requests_to_make, [pbar] * total_requests_to_make)
        for result in results:
            total_data.extend(result)

    if not total_data:
        print(f"No data found for {contest_code}{division}")
        return pd.DataFrame()

    df = pd.DataFrame(total_data)[
        ['rank', 'user_handle', 'score', 'total_time']]

    df['division'] = division
    return df


def get_codechef_contest_rankings(contest_code: str):
    conn = connection()
    try:
        codechef_contest_results = pd.read_sql(
            f'select * from "codechef-{contest_code}"', con=conn)
        # codechef_contest_results = pd.read_csv(
        # f'./codechef_csvs/codechef-{contest_code}.csv')
    except:
        codechef_contest_results = pd.concat([
            download_codechef_contest_data(contest_code, 'A'),
            download_codechef_contest_data(contest_code, 'B'),
            download_codechef_contest_data(contest_code, 'C'),
            download_codechef_contest_data(contest_code, 'D'),
        ])
        codechef_contest_results.to_sql(
            f'codechef-{contest_code}', con=conn, if_exists='replace', index=False)
        # codechef_contest_results.to_csv(
        # f'./codechef_csvs/codechef-{contest_code}.csv', index=False)

    return codechef_contest_results.to_dict('records')


def get_codechef_contest_rankings_of_division(contest_code: str, division: str):
    conn = connection()
    try:
        codechef_contest_results = pd.read_sql(
            f'select * from "codechef-{contest_code}"', con=conn)
        # codechef_contest_results = pd.read_csv(
        # f'./codechef_csvs/codechef-{contest_code}.csv')
    except:
        codechef_contest_results = download_codechef_contest_data(
            contest_code, division)

    codechef_contest_results = codechef_contest_results[
        codechef_contest_results['division'] == division]

    return codechef_contest_results.to_dict('records')


if __name__ == '__main__':
    try:
        for i in range(1, 81):
            print(f"CONTEST: START{i}",
                  get_codechef_contest_rankings(f'START{i}')[0])
    except Exception as e:
        print("API FAILED HERE")
        print(str(e))
