from fastapi import APIRouter, HTTPException
import pandas as pd
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from ..database import codechef_db, students_db
from typing import List
from ..models.models_codechef import CCContestResult, CCFullContestResult


router = APIRouter(prefix='/api/codechef')


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
    if response.status_code != 200 or 'availablePages' not in response.json() or 'list' not in response.json():
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


def read_codechef_contest(contest_code: str):
    conn = codechef_db()
    try:
        codechef_contest_results = pd.read_sql(
            f'select * from "codechef-{contest_code}"', con=conn)
    except:
        contests_with_divisions = ['START', 'COOK', 'LTIME', 'JAN', 'FEB',
                                   'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        for c in contests_with_divisions:
            if c in contest_code:
                dfa = download_codechef_contest_data(contest_code, 'A')
                if dfa.empty:
                    raise HTTPException(404, f"{contest_code} not found")
                dfb = download_codechef_contest_data(contest_code, 'B')
                dfc = download_codechef_contest_data(contest_code, 'C')
                dfd = download_codechef_contest_data(contest_code, 'D')
                codechef_contest_results = pd.concat([dfa, dfb, dfc, dfd])
                break
        else:
            codechef_contest_results = download_codechef_contest_data(
                contest_code, '')
        codechef_contest_results.to_sql(
            f'codechef-{contest_code}', con=conn, if_exists='replace', index=False)
    return codechef_contest_results


@router.get("/{contest_code}")
def get_codechef_contest_rankings(contest_code: str) -> List[CCContestResult]:
    codechef_contest_results = read_codechef_contest(contest_code)
    conn = students_db()
    students = pd.read_sql('select * from students', conn)
    conn.close()
    merged_df = pd.merge(codechef_contest_results, students,
                         left_on='user_handle', right_on='codechef_username', how='inner')
    df = merged_df[merged_df['codechef_username'].notnull()]
    df = df.drop('codechef_username', axis=1)
    return df.to_dict('records')


@router.get("/{contest_code}/full")
def get_codechef_contest_rankings(contest_code: str) -> List[CCFullContestResult]:
    codechef_contest_results = read_codechef_contest(contest_code)
    return codechef_contest_results.to_dict('records')


def get_codechef_contest_rankings_of_division(contest_code: str, division: str):
    conn = codechef_db()
    try:
        codechef_contest_results = pd.read_sql(
            f'select * from "codechef-{contest_code}"', con=conn)
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
