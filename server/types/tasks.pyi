from datetime import datetime
from pydantic import BaseModel

class TaskClass(BaseModel):
    class_id: int
    repeat_next: datetime
    last_modified: datetime
    title: str
    description: str

class TaskInstance(BaseModel):
    instance_id: int
    class_id: int
    date: datetime

