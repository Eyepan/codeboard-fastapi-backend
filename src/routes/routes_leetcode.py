from concurrent.futures import ThreadPoolExecutor
import math
from typing import List
from ..database import leetcode_db, students_db
import pandas as pd
import requests
from fastapi import APIRouter, HTTPException
from tqdm import tqdm

from ..models.models_leetcode import LCContestResult, LCFullContestResult, StudentLeetcode

router = APIRouter(prefix='/api/leetcode')


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
    if response.status_code == 404 or 'user_num' not in response.json() or len(response.json()['total_rank']) == 0:
        raise HTTPException(404, f"Contest {contest_code} doesn't exist")
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


def read_leetcode_contest(contest_code: str):
    conn = leetcode_db()
    try:
        leetcode_contest_results = pd.read_sql(
            f'select * from "leetcode-{contest_code}"', con=conn)
    except:
        leetcode_contest_results = download_leetcode_contest_data(contest_code)
        leetcode_contest_results.to_sql(
            f'leetcode-{contest_code}', con=conn, if_exists='replace', index=False)
    return leetcode_contest_results


@router.get("/{contest_code}")
async def get_leetcode_contest_ratings(contest_code: str) -> List[LCContestResult]:
    leetcode_contest_results = read_leetcode_contest(contest_code)
    conn = students_db()
    students = pd.read_sql('select * from students', conn)
    conn.close()
    merged_df = pd.merge(leetcode_contest_results, students,
                         left_on='username', right_on='leetcode_username', how='inner')
    df = merged_df[merged_df['leetcode_username'].notnull()]
    df = df.drop('leetcode_username', axis=1)
    return df.to_dict('records')


@router.get("/{contest_code}/full")
async def get_all_leetcode_contest_ratings(contest_code: str) -> List[LCFullContestResult]:
    leetcode_contest_results = read_leetcode_contest(contest_code)
    return leetcode_contest_results.to_dict('records')


@router.get("/user/{username}")
async def get_user(username: str):
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
    if response.status_code != 200:
        raise HTTPException(500, f'Something went wrong')
    if 'errors' in response.text:
        raise HTTPException(
            404, f"Student {username} doesn't exist on leetcode")
    response.raise_for_status()
    data = response.json()['data']
    return StudentLeetcode(
        data['matchedUser']['username'],
        data['matchedUser']['profile']['ranking'],
        data['allQuestionsCount'][0]['count'],
        data['matchedUser']['submitStatsGlobal']['acSubmissionNum'][0]['count'],
        data['allQuestionsCount'][1]['count'],
        data['matchedUser']['submitStatsGlobal']['acSubmissionNum'][1]['count'],
        data['allQuestionsCount'][2]['count'],
        data['matchedUser']['submitStatsGlobal']['acSubmissionNum'][2]['count'],
        data['allQuestionsCount'][3]['count'],
        data['matchedUser']['submitStatsGlobal']['acSubmissionNum'][3]['count'],
    ).get_student_leetcode()
