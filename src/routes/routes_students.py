import uuid
from sqlite3 import IntegrityError
from typing import *

import pandas as pd
from fastapi import APIRouter, HTTPException

from ..database import students_db
from ..models.models_students import InStudent, Student

router = APIRouter(prefix='/api/students')


def load_leetcode_data():
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import requests
    import time
    from tqdm import tqdm
    import pandas as pd

    listOfResponses = []

    def get_user(username: str):
        data = {
            "query": """
                query APIReq($username: String!) {
                    matchedUser(username: $username) {
                        username
                        submitStatsGlobal {
                            acSubmissionNum {
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
            listOfResponses.append(response.json())
            raise Exception(response.text)
        if 'errors' in response.text:
            raise Exception(f"Student {username} doesn't exist on leetcode")
        return response.json()['data']

    print("Downloading responses")
    students = pd.read_sql("SELECT * FROM students",
                           con=students_db())
    leetcodeUsernames = [s['leetcode_username'] for s in students.to_dict('records') if s['leetcode_username'] and s['leetcode_username']
                         != '']
    if len(leetcodeUsernames) == 0:
        return
    print(f"There are {len(leetcodeUsernames)} students")
    print("Starting now")
    userData = []
    t = time.time()
    with ThreadPoolExecutor() as executor:
        with tqdm(total=len(leetcodeUsernames)) as pbar:
            futures = [executor.submit(get_user, username)
                       for username in leetcodeUsernames]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    userData.append(result['matchedUser'])
                except Exception as e:
                    print("ERROR: ", e)
                finally:
                    pbar.update(1)
    print("It took ", time.time() - t)
    savableData = []
    for data in userData:
        savableData.append({
            'leetcode_username': data['username'],
            'leetcode_total_problems': data['submitStatsGlobal']['acSubmissionNum'][0]['count'],
            'leetcode_easy_problems': data['submitStatsGlobal']['acSubmissionNum'][1]['count'],
            'leetcode_medium_problems': data['submitStatsGlobal']['acSubmissionNum'][2]['count'],
            'leetcode_hard_problems': data['submitStatsGlobal']['acSubmissionNum'][3]['count'],
        })
    savableData = pd.DataFrame(savableData)

    students = students.merge(savableData, on='leetcode_username', how='left')
    print(students.head())

    students.to_sql("students_with_leetcode", con=students_db(),
                    index=False, if_exists='replace')


@router.get("")
async def get_students():
    conn = students_db()
    df = pd.read_sql('select * from students_with_leetcode', conn)
    conn.close()
    return df.to_dict('records')


@router.get("/student/{id}")
async def get_student_by_id(id: str):
    conn = students_db()
    df = pd.read_sql('select * from students where id = ?', conn, params=(id,))
    conn.close()
    if df.empty:
        raise HTTPException(status_code=404, detail='student not found')
    return df.to_dict('records')[0]


@router.get("/{batch}")
async def get_students_of_batch(batch: str):
    conn = students_db()
    df = pd.read_sql('select * from students_with_leetcode where batch = ?',
                     conn, params=(batch,))
    conn.close()
    return df.to_dict('records')


@router.post("")
async def post_student(student: InStudent):
    conn = students_db()
    student = {
        'id': str(uuid.uuid4()),
        'name': student.name,
        'dept': student.dept,
        'batch': student.batch,
        'leetcode_username': student.leetcode_username,
        'codechef_username': student.codechef_username,
        'codeforces_username': student.codeforces_username
    }
    df = pd.DataFrame(student, index=[0])
    try:
        df.to_sql('students', conn, if_exists='append', index=False)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Student already exists")
    conn.close()


@router.put("")
async def update_student(student: Student):
    conn = students_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * from students_with_leetcode WHERE id = ?', (student.id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=400, detail="Student doesn't exist")
    cursor.execute('UPDATE students SET name = ?, dept = ?, batch = ?, leetcode_username = ?, codechef_username = ?, codeforces_username = ? WHERE id = ?', (
        student.name, student.dept, student.batch, student.leetcode_username, student.codechef_username, student.codeforces_username, student.id))
    conn.commit()
    conn.close()
    return student


@router.delete("")
async def del_student(student: Student):
    conn = students_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * from students_with_leetcode WHERE id = ?', (student.id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=400, detail="Student doesn't exist")
    cursor.execute(
        'DELETE from students_with_leetcode WHERE id = ?', (student.id,))
    conn.commit()
    conn.close()
