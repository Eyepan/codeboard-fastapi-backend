from pydantic import BaseModel


class ProblemsCount(BaseModel):
    difficulty: str
    count: int


class ProblemsPercentage(BaseModel):
    difficulty: str
    percentage: float


class SubmitStatsGlobal(BaseModel):
    acSubmissionNum: list[ProblemsCount]


class Profile(BaseModel):
    ranking: int


class MatchedUser(BaseModel):
    username: str
    profile: Profile
    problemsSolvedBeatsStats: list[ProblemsPercentage]
    submitStatsGlobal: SubmitStatsGlobal


class StudentLeetCodeData(BaseModel):
    allQuestionsCount: list[ProblemsCount]
    matchedUser: MatchedUser
