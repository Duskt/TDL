from pydantic import BaseModel, Field
from typing import TypedDict

class MoodDesc(BaseModel):
    attr_id: int = Field(alias='id')
    body: str
    date: str

MoodBody = TypedDict('MoodBody', {"body": str})
