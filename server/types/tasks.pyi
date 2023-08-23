from pydantic import BaseModel
from datetime import datetime

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

