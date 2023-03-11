from sqlite3 import IntegrityError

from fastapi import HTTPException
from database import connection
import pandas as pd
from models_students import Student
import json


def get_all_students():
    conn = connection()
    df = pd.read_sql('select * from students', conn)
    conn.close()
    return json.loads(df.to_json(orient='records'))


def add_student(student: Student):
    conn = connection()
    df = pd.DataFrame(student.get_student(), index=[0])
    try:
        df.to_sql('students', conn, if_exists='append', index=False)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Student already exists")
    conn.close()


def update_student(student: Student):
    conn = connection()
    df = pd.DataFrame(student.get_student(), index=[0])
    df.to_sql('students', conn, if_exists='replace', index=False)
    conn.close()


def delete_student(student: Student):
    conn = connection()
    cursor = conn.cursor()
    # TODO: raise exception if user doesn't exist
    cursor.execute('DELETE FROM students WHERE id = ?', (student.id,))
    conn.commit()
    conn.close()
