from fastapi import APIRouter
from models_students import Student
from utils_students import get_all_students, add_student, update_student, delete_student


router = APIRouter(prefix='/api/students')


@router.get("")
async def get_students():
    return get_all_students()


@router.post("")
async def post_student(student: Student):
    add_student(student)


@router.put("")
async def put_student(student: Student):
    update_student(student)


@router.delete("")
async def del_student(student: Student):
    delete_student(student)
