from pydantic import BaseModel
from typing import List


class ProblemsCount(BaseModel):
    difficulty: str
    count: int


class ProblemsPercentage(BaseModel):
    difficulty: str
    percentage: float


class SubmitStatsGlobal(BaseModel):
    acSubmissionNum: List[ProblemsCount]


class Profile(BaseModel):
    ranking: int


class MatchedUser(BaseModel):
    username: str
    profile: Profile
    problemsSolvedBeatsStats: List[ProblemsPercentage]
    submitStatsGlobal: SubmitStatsGlobal


class StudentLeetCodeData(BaseModel):
    allQuestionsCount: List[ProblemsCount]
    matchedUser: MatchedUser

    # df = df[['username', 'rank', 'score', 'finish_time']]


class ContestResult(BaseModel):
    username: str
    rank: int
    score: int
    name: str
    dept: str
    batch: str
    codechef_username: str
    codeforces_username: str
# username  rank  score  name dept  batch codechef_username codeforces_username


# File "/app/src/models/models_leetcode.py", line 15, in SubmitStatsGlobal
# acSubmissionNum: List[ProblemsCount]
# TypeError: 'type' object is not subscriptable
