from pydantic import BaseModel


class Student(BaseModel):
    id: str
    name: str
    dept: str
    batch: str
    leetcode_username: str
    codechef_username: str
    codeforces_username: str

    def __init__(self, id, name, dept, batch, leetcode_username, codechef_username, codeforces_username):
        super().__init__(
            id=id,
            name=name,
            dept=dept,
            batch=batch,
            leetcode_username=leetcode_username,
            codechef_username=codechef_username,
            codeforces_username=codeforces_username
        )

    def get_student(self):
        return super().__dict__


class InStudent(BaseModel):
    name: str
    dept: str
    batch: str
    leetcode_username: str
    codechef_username: str
    codeforces_username: str
