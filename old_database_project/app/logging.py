import time
from .models import Logs, db

def log_standing_selection(username, yearID, team_name):
    new_log_entry = Logs(username = username, yearID = yearID, team_name = team_name, timestamp = int(time.time()))

    db.session.add(new_log_entry)
    db.session.commit()