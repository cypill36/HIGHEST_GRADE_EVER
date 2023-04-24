from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, StatsForm
import pymysql
from app import csi3335sp2023 as cfg


user = {'username': ''}


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():  # not actually doing anything
    global user
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        user['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


team_name = None
team_id = None
year = None
years = None


@app.route('/index/<team>', methods=['GET', 'POST'])
def index(team):
    print("launching")
    global user, team_name, year, team_id, years
    form = StatsForm()
    con = pymysql.connect(host=cfg.mysql['location'],
                          user=cfg.mysql['user'],
                          password=cfg.mysql['password'],
                          database=cfg.mysql['database'])
    try:
        post = False
        team_names = []
        cur = con.cursor()
        sql = 'SELECT DISTINCT team_name FROM teams'
        cur.execute(sql)
        results = cur.fetchall()
        for name in results:
            team_names.append(name[0])
        if request.method == 'POST':
            print("POST")
            post = True
            team_name = request.form.get('team_name')
        else:
            team_name = team
        print(team_name)
        if team_name is None or team_name == "" or team_name == "None":
            print("select a team")
            return render_template('stats.html', form=form, title='Baseball Stats', user=user, team_picked=True,
                                   teams=team_names)
        elif not form.is_submitted():
            form.year.default = None
            print("select a year")
            sql = 'SELECT teamid FROM teams WHERE team_name=%s'
            cur.execute(sql, team_name)
            team_id = cur.fetchall()[0][0]
            print(team_id)
            sql = 'SELECT DISTINCT yearid FROM teams WHERE team_name=%s'
            cur.execute(sql, team_name)
            results = cur.fetchall()
            years = []
            for year in results:
                years.append(year[0])
            form.year.choices = [(index, year) for index, year in enumerate(years, start=1)]
            return render_template('stats.html', form=form, title='Baseball Stats', user=user, team_picked=False,
                                   teams=team_names, team_name=team_name)
        elif post:
            print("we got your submit!")
            year = form.year.data
            form.year.default = year
            form.process()
            sql = '''SELECT 
                            playerID,
                            position,
                            SUM(f_G) 
                        FROM fielding
                        WHERE teamID=%s AND yearid=%s
                        GROUP BY playerID, position'''
            cur.execute(sql, [team_id, year])
            results = cur.fetchall()
            players = {}
            for row in results:
                if row[0] not in players.keys():
                    players[row[0]] = {}
                players[row[0]][row[1]] = row[2]
            players_by_name = {}
            for playerid in players.keys():
                sql = '''SELECT CONCAT(nameFirst + ' ' + nameLast) FROM people WHERE playerID=%s'''
                cur.execute(sql, playerid)
                player_name = cur.fetchall()[0][0]
                players_by_name[player_name] = players[playerid]
                sql = '''SELECT b_H/b_AB, (b_H + b_BB + b_HBP)/(b_AB + b_BB + b_HBP + b_SF), 
                        ((b_R - b_2B - b_3B - b_HR) + (2 * b_2B) + (3 * b_3B) + (4 * b_HR)) / b_AB
                         FROM batting
                         WHERE playerid=%s AND yearId=%s AND teamID=%s'''
                cur.execute(sql, [playerid, year, team_id])
                results = cur.fetchone()
                players_by_name[player_name]['batting_avg'] = results[0]
                players_by_name[player_name]['obp'] = results[1]
                players_by_name[player_name]['slg'] = results[3]
                # TODO: get pitching data
            return render_template('stats.html', form=form, title='Baseball Stats', user=user, team_picked=False,
                                   teams=team_names, team_name=team_name, batting_data=players_by_name)
    except Exception:
        con.rollback()
        print("Database Exception.")
        raise
    else:
        con.commit()
    finally:
        con.close()
    return render_template('stats.html', form=form, title='Baseball Stats', user=user)

