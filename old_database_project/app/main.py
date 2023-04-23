from flask import Blueprint, render_template, redirect, url_for, request, jsonify
<<<<<<< HEAD
from .models import Teams, Divisions, Leagues, db
from flask_login import login_required, current_user
=======
from .models import Teams, Divisions, Leagues, Logs, Seriespost, db
from .logging import log_standing_selection
from flask_login import login_required, current_user
from datetime import datetime
>>>>>>> 3e95c82985593e0e87eec8301c088e9f6d3e6601

main_bp = Blueprint("main_bp", __name__,
                    template_folder="templates", static_folder="static", static_url_path="/auth/static")


@main_bp.route("/")
@login_required
def home():
    teams = Teams.query.group_by(Teams.team_name).all()
    return render_template("stats/home.html", user=current_user, teams=teams)

@main_bp.route("/standings")
@login_required
def standings():
    team_name = request.args.get("team_name")
    year_id = request.args.get("year_id")

    divisions_query = Teams.query.filter_by(team_name = team_name, yearID = year_id).all()
    
    lg_id = divisions_query[0].lgID
    division_id = divisions_query[0].divID

    standings_query = Teams.query.filter_by(yearID = year_id, divID = division_id, lgID = lg_id).order_by(Teams.team_W.desc()).all()
    
    division_name = None
    league_name = None
    if division_id is not None:
        division_name = Divisions.query.filter_by(divID = division_id, lgID = lg_id ).all()[0].division_name
    else:
        league_name = Leagues.query.filter_by(lgID = lg_id).all()[0].league_name

    leader_wins = standings_query[0].team_W

    standings = []
    for team in standings_query:

<<<<<<< HEAD
=======
        # Check if team made playoffs
        playoff_win_query = Seriespost.query.filter_by(yearID = team.yearID, teamIDloser = team.teamID).all()
        playoff_lose_query = Seriespost.query.filter_by(yearID = year_id, teamIDwinner = team.teamID).all()

        if len(playoff_win_query) > 0 or len(playoff_lose_query) > 0:
            made_playoffs = True
        else:
            made_playoffs = False

>>>>>>> 3e95c82985593e0e87eec8301c088e9f6d3e6601
        standings.append({
            "rank": standings_query.index(team) + 1,
            "teamID": team.teamID,
            "name": team.team_name,
            "wins": team.team_W,
            "losses": team.team_L,
            "win_percentage": round((team.team_W / (team.team_W + team.team_L)) * 100, 2),
            "games_behind": leader_wins - team.team_W,
<<<<<<< HEAD
            "team_name": team.team_name
        })

    return render_template("stats/standings.html", user=current_user, standings=standings, team_name=team_name, year_id=year_id, division_name=division_name, league_name=league_name)
    
=======
            "team_name": team.team_name,
            "made_playoffs": made_playoffs
        })

    log_standing_selection(current_user.username, year_id, team_name)

    return render_template("stats/standings.html", user=current_user, standings=standings, team_name=team_name, year_id=year_id, division_name=division_name, league_name=league_name)

@main_bp.route("/playoffs")
@login_required
def playoffs():
    team_name = request.args.get("team_name")
    year_id = request.args.get("year_id")

    playoff_query = Seriespost.query.filter_by(yearID = year_id).all()

    return render_template("stats/playoffs.html", user=current_user, year_id=year_id, team_name=team_name, playoffs=playoff_query)
>>>>>>> 3e95c82985593e0e87eec8301c088e9f6d3e6601

@main_bp.route("/admin")
@login_required
def admin():
    if current_user.isAdmin:
<<<<<<< HEAD
        return render_template("admin/admin.html")
=======
        logs = Logs.query.all()
        
        logs_json = []
        for log in logs:
            logs_json.append({
                "username": log.username,
                "team_name": log.team_name,
                "yearID": log.yearID,
                "timestamp": datetime.utcfromtimestamp(log.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            })

        return render_template("admin/admin.html", user=current_user, logs=logs_json)
>>>>>>> 3e95c82985593e0e87eec8301c088e9f6d3e6601
    else:
        return redirect(url_for("main_bp.home"))

@main_bp.route("/get_years")
def get_years():
    team_name = request.args.get("team_name")
<<<<<<< HEAD

=======
>>>>>>> 3e95c82985593e0e87eec8301c088e9f6d3e6601
    years = Teams.query.filter_by(team_name=team_name).order_by(Teams.yearID).all()

    years_json = []
    for year in years:
        years_json.append(year.yearID)

    return jsonify(years_json)