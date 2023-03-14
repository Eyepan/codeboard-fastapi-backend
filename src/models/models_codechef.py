from pydantic import BaseModel


class CCContestResult(BaseModel):
    username: str
    rank: int
    score: int
    division: str
    name: str
    dept: str
    batch: str
    leetcode_username: str
    codeforces_username: str


class CCFullContestResult(BaseModel):
    username: str
    rank: int
    score: int
    division: str
