import json
import uuid
from sqlite3 import IntegrityError
from typing import *

import pandas as pd
from fastapi import APIRouter, HTTPException

from ..database import connection
from ..models.models_students import InStudent, Student

router = APIRouter(prefix='/api/students')


@router.get("")
async def get_students() -> List[Student]:
    conn = connection()
    df = pd.read_sql('select * from students', conn)
    conn.close()
    return json.loads(df.to_json(orient='records'))


@router.get("/student/{id}")
async def get_student_by_id(id: str) -> Student:
    conn = connection()
    df = pd.read_sql('select * from students where id = ?', conn, params=(id,))
    conn.close()
    if df.empty:
        raise HTTPException(status_code=404, detail='student not found')
    return json.loads(df.to_json(orient='records'))[0]


@router.get("/{batch}")
async def get_students_of_batch(batch: str) -> List[Student]:
    conn = connection()
    df = pd.read_sql('select * from students where batch = ?',
                     conn, params=(batch,))
    conn.close()
    return json.loads(df.to_json(orient='records'))


@router.post("")
async def post_student(student: InStudent):
    conn = connection()
    student = Student(id=str(uuid.uuid4()), name=student.name, dept=student.dept, batch=student.batch, leetcode_username=student.leetcode_username,
                      codechef_username=student.codechef_username, codeforces_username=student.codeforces_username)
    df = pd.DataFrame(student.get_student(), index=[0])
    try:
        df.to_sql('students', conn, if_exists='append', index=False)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Student already exists")
    conn.close()


@router.put("")
async def put_student(student: Student):
    conn = connection()
    df = pd.DataFrame(student.get_student(), index=[0])
    df.to_sql('students', conn, if_exists='replace', index=False)
    conn.close()


@router.delete("")
async def del_student(student: Student):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE id = ?', (student.id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=400, detail="Student doesn't exist")
    cursor.execute('DELETE FROM students WHERE id = ?', (student.id,))
    conn.commit()
    conn.close()
