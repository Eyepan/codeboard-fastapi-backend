from pydantic import BaseModel


class CCContestResult(BaseModel):
    user_handle: str
    rank: int
    score: int
    division: str
    name: str
    dept: str
    batch: str
    leetcode_username: str
    codeforces_username: str


class CCFullContestResult(BaseModel):
    user_handle: str
    rank: int
    score: int
    division: str
