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
        return redirect(url_for('index', teamName='None'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect( url_for('login') )
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', teamName='None')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


team_name = None


@app.route('/index/<teamName>', methods = ['GET', 'POST'])
@login_required
def index():
    sql = '''SELECT DISTINCT(yearid)
             FROM teams
             WHERE team_name=%s
    '''
    years = []
    cur = con.cursor()
    disabled = True
    if teamName is not None and teamName != 'None':
        cur.execute(sql, teamName)
        disabled = False
        results = cur.fetchall()
        for row in results:
            years.append(int(row[0]))
    teams = []
    
    sql = ''' select distinct(team_name) from teams order by team_name ; '''
    cur.execute(sql)
    results = cur.fetchall()
    for x in results:
        teams.append(x[0])
    if not disabled:
        form.yearchoices = [(index, year) for index, year in enumerate(years, start=1)]
    #sql = '''  select distinct(yearid) from teams where teamId = %s order be yearid ; '''
    #cur.execute(sql)
    #results2 = cur.fetchall()
    #for x in results2:
    #    years.append(x[0])
    return render_template("index.html", title='Home Page',teams=teams, team_picked=disabled, team_name=teamName, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index', teamName=None))
   

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index', teamName='None'))
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
        
        # get teamID

        sql = '''SELECT teamID 
                 FROM teams
                 WHERE team_name = %s AND yearID = %s'''

        cur.execute( sql, [ chosenTeam, chosenYear ] )
        
        print( sql % ( chosenTeam, chosenYear ) )

        chosenTeamID = cur.fetchall()[0][0]
        print(chosenTeamID)

        # Getting roster 
        sql = '''SELECT CONCAT(nameFirst, ' ', nameLast) 
                 FROM people 
                 WHERE playerid IN (
                    SELECT DISTINCT(playerid) 
                    FROM batting 
                    WHERE yearID = %s AND teamID = (
                        SELECT DISTINCT(teamid) 
                        FROM teams 
                        WHERE team_name = %s AND yearID = %s));'''
        

        #print( sql % ( chosenYear, chosenTeam, chosenYear ) )

        params = [ chosenYear, chosenTeam, chosenYear ]
        cur.execute(sql, params)
        roster = cur.fetchall()
        
        rosterList = []
        battingStats = {}
        pitchingStats = {}
        playerIDs = []
        toDelete = []
        for row in roster:
            for col in row:
                rosterList.append(col)

                # getting playerid for each player
                sql = '''SELECT DISTINCT(playerid) 
                         FROM people
                         WHERE nameFirst = %s AND nameLast = %s'''
                cur.execute( sql, col.rsplit(' ', 1) )
                #print( col )
                playerID = cur.fetchall()[0][0]

                battingStats[ playerID ] = [ col, 0, 0, 0, 0, 0, 0, 0, 0 ]
                pitchingStats[ playerID ] = [ col, 0 ]

        positionCounts = { 'C':1, '1B':2, '2B':3, '3B':4, 'SS':5, 'LF':6, 'CF':7, 'RF':8 }	

        for playerID in battingStats.keys():
            
            # getting batting stats for each player
            sql = '''SELECT position, SUM(f_G) AS 'Games Played' 
                     FROM fielding
                     WHERE teamID=%s AND yearid=%s AND playerid=%s
                     GROUP BY playerID, position
                  '''
            cur.execute( sql, [ chosenTeamID, chosenYear, playerID ] )
            curStats = cur.fetchall()

            #print( sql % ( chosenTeamID, chosenYear, playerID ) )

            for row in curStats:
                if row[0] == 'P':
                    pitchingStats[ playerID ][ 1 ] = row[1]
                    #del battingStats[ playerID ]
                else:
                    battingStats[ playerID ][ positionCounts[ row[0] ] ] = row[1]

            sql = '''SELECT b_H/b_AB, (b_H + b_BB + b_HBP)/(b_AB + b_BB + b_HBP + b_SF), 
            ((b_R - b_2B - b_3B - b_HR) + (2 * b_2B) + (3 * b_3B) + (4 * b_HR)) / b_AB
                 FROM batting
                 WHERE playerid=%s AND yearId=%s AND teamID=%s'''

            cur.execute( sql, [ playerID, chosenYear, chosenTeamID ] )
            
            last3Stats = cur.fetchall()

            if len( last3Stats ) == 0:
                toDelete.append(playerID)
            for row in last3Stats:
                for col in row:
                    battingStats[ playerID ].append( col )

            playerIDs.append( playerID )
        
        for playerID in playerIDs:
            if pitchingStats[ playerID ][ 1 ] == 0:
                del pitchingStats[ playerID ]
            else:
                del battingStats[ playerID ]

        for playerID in toDelete:
            del battingStats[ playerID ]

        #print( pitchingStats )

    except Exception:
        con.rollback()
        print("Database Exception.")
        raise
    else:
        con.commit()
    return render_template('stats.html', title = 'stats', chosenTeam = chosenTeam, chosenYear = chosenYear, roster = rosterList, battingStats = battingStats)


