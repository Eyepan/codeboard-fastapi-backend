from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    dept: str
    year: int
    leetcode_username: str
    codechef_username: str
    codeforces_username: str

    def __init__(self, id, name, dept, year, leetcode_username, codechef_username, codeforces_username):
        super().__init__(id=id, name=name, dept=dept, year=year, leetcode_username=leetcode_username,
                         codechef_username=codechef_username, codeforces_username=codeforces_username)

    def get_student(self):
        return super().__dict__
