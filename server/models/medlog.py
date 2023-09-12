from api import BaseModel


class MoodDesc(BaseModel):
    body: str
    date: str


class MoodDescGETReq(BaseModel):
    date: str


class MoodDescGETRes(BaseModel):
    body: str | None
