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

from api import do_logging, get_from_db, model_cast
from flask import Response, request
from pydantic import ValidationError
from models.medlog import MoodDescGETReq, MoodDescGETRes

DBPATH = "app.db"
DEFAULT_MOODDESC = "Default"


@do_logging()
def get_mood_desc():
    try:
        params = MoodDescGETReq(**request.args)
    except ValidationError:
        print(f"Invalid GET request {request.args=}")
        return Response(json.dumps({"success": False}), 400)

    keys = ("body",)
    r = get_from_db(keys, {"date": params.date}, "journalentries")
    m = model_cast(keys, r, MoodDescGETRes)

    resp = {"success": True, "payload": dict(m)}
    return resp


@do_logging()
def post_mood_desc():
    conn = sqlite3.connect(DBPATH)
    conn.execute(
        """
        INSERT OR REPLACE INTO journalentries (date, body)
        VALUES(?, ?);
    """,
        (request.form["date"], request.form["desc"]),
    )
    conn.commit()
    return {"success": True}
