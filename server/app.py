import logging
from flask import Flask
from endpoints.tasks import post_taskclass, get_today, post_taskinstance
from endpoints.medlog import post_mood_desc, get_mood_desc
import dotenv

config = dotenv.dotenv_values(dotenv.find_dotenv())
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.logger.level = logging.DEBUG
DBPATH = "app.db"


app.get("/api/tasks/today")(get_today)
app.post("/api/tasks/taskclass")(post_taskclass)
app.post("/api/tasks/taskinstance")(post_taskinstance)

app.get("/api/log/mooddesc")(get_mood_desc)
app.put("/api/log/mooddesc")(post_mood_desc)

"""
$ flask run
__name__ = app
$ python3 app.py
__name__ = __main__
"""
if __name__ == "__main__":
    app.run(config.get("HOST"), debug=True)
