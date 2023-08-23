"""
Medlogs:
- Once a day, you can create / edit a description of your mood.
- Once a day, you can answer a short mental health questionnaire for a more scientific angle of your mental health.

Other ideas:
- Record a 'medication' similarly to Apple's health app, and record instances of taking a dosage.
- Integrate Apple health app (use that directly instead of duplicating functionality).
"""
import json
import sqlite3
from typing import Optional

from flask import Response, request
from lightapi import BaseModel, do_logging
from pydantic import Field, ValidationError

DBPATH = "app.db"


class MoodDesc(BaseModel):
    _id: int = Field(alias="id")
    body: str
    date: str


class GetMoodDescReq(BaseModel):
    date: str


class GetMoodDescResp(BaseModel):
    body: str
    _id: Optional[int] = Field(alias="id", default=None)


def get_mood_desc():
    try:
        params = GetMoodDescReq(**request.args)
    except ValidationError as _:
        print(f"Invalid GET request {request.args=}")
        return Response(json.dumps({"success": False}), 400)

    values = ("body",)
    conn = sqlite3.connect(DBPATH)
    r = conn.execute(
        f"""
        SELECT {', '.join(values)} FROM journalentries WHERE date=?;
    """,
        (params.date,),
    ).fetchone()
    resp = {
        "success": True,
        "payload": dict(
            GetMoodDescResp(**dict(zip(values, r)))
            if r
            else GetMoodDescResp(body="Default")
        ),
    }
    return resp


@do_logging()
def post_mood_desc():
    conn = sqlite3.connect(DBPATH)
    conn.execute(
        """
        INSERT OR REPLACE INTO journalentries (body)
        VALUES(?);
    """,
        (request.form["desc"],),
    )
    conn.commit()
    return {"success": True}
