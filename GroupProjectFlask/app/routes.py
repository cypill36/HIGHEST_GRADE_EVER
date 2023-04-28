from flask import render_template, session, flash, get_flashed_messages, redirect, request, Flask, url_for
from app import db, app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.urls import url_parse
import pymysql
import sys
import warnings
import csi3335 as cfig

#CHANGE
#con = pymysql.connect(host='localhost', user='yassenarab', password='YA2002ya', database='baseball')
con = pymysql.connect(host=cfig.con['host'], user=cfig.con['user'], password=cfig.con['password'], database=cfig.con['database'])


@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect( url_for('login') )
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    teams = []
    years = []
    cur = con.cursor()
    sql = ''' select distinct(team_name) from teams order by team_name ; '''
    cur.execute(sql)
    results = cur.fetchall()
    for x in results:
        teams.append(x[0])
    sql = '''  select distinct(yearid) from teams order by yearid ; '''
    cur.execute(sql)
    results2 = cur.fetchall()
    for x in results2:
        years.append(x[0])
    return render_template("index.html", title='Home Page',teams=teams, years = years)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
   

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form =  RegistrationForm()
    print( form.validate_on_submit() )
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/submit-form', methods=['POST'])
@login_required
def submit_form():
    
    # Get user selected team and year and pass into the submit 
    chosenTeam = request.form['team']
    chosenYear = request.form['year']
    #session[ 'chosenTeam' ] = request.form['team']
    #session[ 'chosenYear' ] = request.form['year']

    # Run query to get the roster
    roster = []

    try:
        cur = con.cursor()
        sql = '''SELECT CONCAT(nameFirst, ' ', nameLast) FROM people WHERE playerid IN (SELECT DISTINCT(playerid) FROM batting WHERE yearID = %s AND teamID = (SELECT DISTINCT(teamid) FROM teams WHERE team_name = %s LIMIT 1));'''
        params = [ chosenYear, chosenTeam ]
        cur.execute(sql, params)
        roster = cur.fetchall()
        
        rosterList = []
        for row in roster:
            for col in row:
                rosterList.append(col)

    except Exception:
        con.rollback()
        print("Database Exception.")
        raise
    else:
        con.commit()
    return render_template('stats.html', title = 'stats', chosenTeam = chosenTeam, chosenYear = chosenYear, roster = rosterList)



