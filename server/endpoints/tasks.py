import datetime
import sqlite3

from flask import redirect, request
from pydantic import BaseModel

DBPATH = "app.db"


class Task(BaseModel):
    title: str
    description: str
    done: bool
    instance_id: int

    def __post_init__(self):
        # bool stored as int(?) in db
        self.done = True if self.done else False


def get_today():
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT instance_id, title, description, done 
        FROM taskinstances JOIN taskclasses USING(class_id)
        WHERE date = ?;
    """,
        (str(datetime.date.today()),),
    )
    tasks = [Task(**i) for i in cur.fetchall()]
    resp = {"success": True, "payload": [i for i in tasks]}
    return resp


def post_taskclass():
    data = request.form
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO taskclasses (title, description)
        VALUES(?, ?);
    """,
        (data["title"], data["description"]),
    )
    conn.commit()
    return redirect("/")


def insert_taskinstance(class_id: int, date: datetime.date | str):
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO taskinstances (class_id, date, done)
        VALUES(?, ?, FALSE);
    """,
        (class_id, str(date)),
    )
    conn.commit()


def post_taskinstance():
    data = request.form
    insert_taskinstance(int(data["class_id"]), data["date"])
    return redirect("/")
