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


# a sample json body for a request containing a student
# {
#     "id": 1,
#     "name": "John Doe",
#     "dept": "CSE",
#     "year": 2,
#     "leetcode_username": "johndoe",
#     "codechef_username": "johndoe",
#     "codeforces_username": "johndoe"
# }
