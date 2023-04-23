from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean, default=False)

class Teams(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    teamID = db.Column(db.String(3))
    yearID = db.Column(db.Integer)
    team_name = db.Column(db.String(50))
    lgID = db.Column(db.String(2))
    divID = db.Column(db.String(1))
    team_W = db.Column(db.Integer)
    team_L = db.Column(db.Integer)

class Divisions(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    divID = db.Column(db.String(2))
    lgID = db.Column(db.String(2))
    division_name = db.Column(db.String(50))

class Leagues(db.Model):
    lgID = db.Column(db.String(2), primary_key=True)
<<<<<<< HEAD
    league_name = db.Column(db.String(50))
=======
    league_name = db.Column(db.String(50))

class Logs(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    team_name = db.Column(db.String(50))
    yearID = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

class Seriespost(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    teamIDwinner = db.Column(db.String(3))
    teamIDloser = db.Column(db.String(3))
    yearID = db.Column(db.Integer)
    round = db.Column(db.String(5))
    wins = db.Column(db.Integer)
    loses = db.Column(db.Integer)
    ties = db.Column(db.Integer)
>>>>>>> 3e95c82985593e0e87eec8301c088e9f6d3e6601
