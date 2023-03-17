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


class StudentLeetcode(BaseModel):
    username: str
    ranking: int
    totalQuestionsCount: int
    totalQuestionsSolved: int
    easyQuestionsCount: int
    easyQuestionsSolved: int
    mediumQuestionsCount: int
    mediumQuestionsSolved: int
    hardQuestionsCount: int
    hardQuestionsSolved: int

    def __init__(self, u, r, tqc, tqs, eqc, eqs, mqc, mqs, hqc, hqs):
        super().__init__(
            username=u,
            ranking=r,
            totalQuestionsCount=tqc,
            totalQuestionsSolved=tqs,
            easyQuestionsCount=eqc,
            easyQuestionsSolved=eqs,
            mediumQuestionsCount=mqc,
            mediumQuestionsSolved=mqs,
            hardQuestionsCount=hqc,
            hardQuestionsSolved=hqs)

    def get_student_leetcode(self):
        return super().__dict__


class LCContestResult(BaseModel):
    username: str
    rank: int
    score: int
    name: str
    dept: str
    batch: str
    codechef_username: str
    codeforces_username: str


class LCFullContestResult(BaseModel):
    username: str
    rank: int
    score: int
