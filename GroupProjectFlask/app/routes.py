from flask import render_template, session, flash, get_flashed_messages, redirect, request, Flask, url_for
from app import db, app
from app.forms import LoginForm, RegistrationForm, StatsForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.urls import url_parse
import pymysql
import sys
import warnings
import csi3335 as cfig
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


#need to add this packege.
#from flask_moment import Moment

con = pymysql.connect(host=cfig.con['host'], user=cfig.con['user'], password=cfig.con['password'],
                      database=cfig.con['database'])
cur = con.cursor()
sql1 = ''' CREATE TABLE IF NOT EXISTS users (id VARCHAR(50), team_name VARCHAR(50), yearid INT); '''
cur.execute(sql1)

@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    con = pymysql.connect(host=cfig.con['host'], user=cfig.con['user'], password=cfig.con['password'],
                      database=cfig.con['database'])
    if current_user.is_authenticated:
        cur = con.cursor()
        # make the table and update it for the admin
    
        sql1 = ''' CREATE TABLE IF NOT EXISTS users (id VARCHAR(50), team_name VARCHAR(50), yearid INT); '''
        cur.execute(sql1)
        return redirect(url_for('index', teamName='None'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', teamName='None')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


global stats_form


@app.route('/index/<first>/<second>', methods=['GET'])
def redirectToIndex(first, second):
    return redirect(url_for('index', teamName=first + '?' + second))


@app.route('/submit-form/<first>/<second>', methods=['GET'])
def redirectToSubmitForm(first, second):
    print('hi')
    return redirect(url_for('submit_form', teamName=first + '?' + second))


global team_name, year_id


@app.route('/index/<teamName>', methods=['GET', 'POST'])
@login_required
def index(teamName):
    con = pymysql.connect(host=cfig.con['host'], user=cfig.con['user'], password=cfig.con['password'],
                      database=cfig.con['database'])
    global stats_form
    stats_form = StatsForm()

    sql = '''SELECT DISTINCT(yearid)
             FROM teams
             WHERE team_name=%s
    '''
    years = []
    cur = con.cursor()

    disabled = True
    if teamName is not None and teamName != 'None' and teamName != ' ':
        if '?' in teamName:
            teamName = teamName.replace('?', '/')
        # print('getting years for ' + teamName)
        team_name = teamName
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
        if '/' in teams[-1]:
            teams[-1].replace('/', '\\')
    if not disabled:
        # print('setting year choices: ')
        # print(years)
        stats_form.year.choices = [(index, year) for index, year in enumerate(years, start=1)]
    # sql = '''  select distinct(yearid) from teams where teamId = %s order be yearid ; '''
    # cur.execute(sql)
    # results2 = cur.fetchall()
    # for x in results2:
    #    years.append(x[0])
    if request.method == 'POST' and teamName != 'None':
        # if stats_form.validate_on_submit():
        return redirect(url_for('submit_form', teamName=teamName))
    return render_template("index.html", title='Home Page', teams=teams, team_picked=disabled, team_name=teamName,
                           form=stats_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index', teamName='None'))
    form = RegistrationForm()
    # print( form.validate_on_submit() )
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# @app.route('/index', methods=['GET', 'POST'])
# def index():
# return redirect(url_for('index', teamName='None'))


@app.route('/submit-form/<teamName>', methods=['GET', 'POST'])
@login_required
def submit_form(teamName):
    con = pymysql.connect(host=cfig.con['host'], user=cfig.con['user'], password=cfig.con['password'],
                      database=cfig.con['database'])
    global stats_form, team_name
    # if not stats_form.validate_on_submit():
    # return redirect(url_for('index', teamName='None'))
    # Get user selected team and year and pass into the submit
    chosenTeam = teamName
    if '?' in chosenTeam:
        chosenTeam = chosenTeam.replace('?', '/')
    chosenYear = stats_form.year.choices[stats_form.year.data - 1][1]
    print(str(chosenYear), chosenTeam)
    # session[ 'chosenTeam' ] = request.form['team']
    # session[ 'chosenYear' ] = request.form['year']
    if chosenTeam is None or chosenTeam == 'None':
        redirect(url_for('index', teamName='None'))
    # Run query to get the roster
    roster = []

    try:
        cur = con.cursor()
 
        # make the table and update it for the admin
    
        sql1 = ''' CREATE TABLE IF NOT EXISTS users (id VARCHAR(50), team_name VARCHAR(50), yearid INT); '''
        cur.execute(sql1)

        id = current_user.username       
        sql2 = ''' insert into users values(%s,%s,%s); '''
        cur.execute(sql2, [id, chosenTeam, chosenYear])
          
        # get teamID

        sql = '''SELECT teamID 
                 FROM teams
                 WHERE team_name = %s AND yearID = %s'''

        cur.execute(sql, [chosenTeam, chosenYear])

        # print( sql % ( chosenTeam, chosenYear ) )

        chosenTeamID = cur.fetchall()[0][0]
        # print(chosenTeamID)
        # print(chosenTeamID)

        get_player_ids_sql = '''SELECT DISTINCT(playerid)
                                FROM batting
                                WHERE yearID = %s AND teamID = %s'''
        get_dh_ids_sql = '''SELECT DISTINCT(playerid)
                                 FROM batting
                                 WHERE yearid = %s AND teamid = %s
                                    AND playerid NOT IN (
                                        SELECT DISTINCT(playerid)
                                        FROM fielding
                                    )
        '''

        # print(get_player_ids_sql % (chosenYear, chosenTeamID))
        cur.execute(get_player_ids_sql, [chosenYear, chosenTeamID])
        ids = cur.fetchall()
        playerIDs = []
        for row in ids:
            playerIDs.append(row[0])

        cur.execute(get_dh_ids_sql, [chosenYear, chosenTeamID])
        DHs = []
        results = cur.fetchall()
        for dh_id in results:
            DHs.append(dh_id[0])
        # print(sql % (chosenYear, chosenTeam, chosenYear))

        rosterList = []
        battingStats = {}
        pitchingStats = {}
        toDelete = []

        for player in playerIDs:

            get_player_name_sql = '''SELECT CONCAT(nameFirst, ' ', nameLast)
                                     FROM people
                                     WHERE playerID=%s'''
            cur.execute(get_player_name_sql, player)
            results = cur.fetchone()
            if len(results) != 0:
                rosterList.append(results[0])
                battingStats[player] = [results[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                pitchingStats[player] = [results[0], 0, 0]

        positionCounts = {'C': 2, '1B': 3, '2B': 4, '3B': 5, 'SS': 6, 'LF': 7, 'CF': 8, 'RF': 9}

        for playerID in battingStats.keys():
            get_total_games_sql = '''SELECT SUM(f_G) FROM fielding WHERE teamid=%s AND yearid=%s AND playerid=%s
                                     GROUP BY teamid, yearid, playerid
            '''
            if playerID in DHs:
                get_total_games_sql.replace('f_G', 'b_G')
                get_total_games_sql.replace('fielding', 'batting')

            cur.execute(get_total_games_sql, [chosenTeamID, chosenYear, playerID])
            games = cur.fetchall()
            if len(games) > 0:
                games = games[0][0]
            else:
                games = 0
            battingStats[playerID][1] = games
            if playerID in DHs:
                battingStats[playerID][10] = games
            # getting batting stats for each player
            sql = '''SELECT position, SUM(f_G) AS 'Games Played', SUM(f_GS) AS 'Games Started' 
                     FROM fielding
                     WHERE teamID=%s AND yearid=%s AND playerid=%s
                     GROUP BY playerID, position
                  '''
            cur.execute(sql, [chosenTeamID, chosenYear, playerID])
            curStats = cur.fetchall()

            #print(sql % (chosenTeamID, chosenYear, playerID))

            for row in curStats:
                if row[0] == 'P':
                    pitchingStats[playerID][1] = row[1]
                    pitchingStats[playerID][2] = (row[2])

                    pitching_sql = '''SELECT FLOOR(SUM(IFNULL(p_IPOuts, 0)/3)) AS 'IP', 
                                        SUM(IFNULL(p_H, 0) + IFNULL(p_BB, 0))/(SUM(IFNULL(p_IPOuts, 0)/3)) AS WHIP,
                                        (SUM(IFNULL(p_SO, 0)) * 9)/SUM(IFNULL(p_IPOuts, 0)/3) AS Kper9,
                                        SUM(IFNULL(p_BB, 0)) AS BB
                                      FROM pitching
                                      WHERE teamID=%s AND yearid=%s AND playerID=%s
                    '''
                    cur.execute(pitching_sql, [chosenTeamID, chosenYear, playerID])
                    results = cur.fetchone()

                    for statistic in results:
                        pitchingStats[playerID].append(statistic)
                    #print(pitchingStats)
                    # del battingStats[ playerID ]
                elif row[0] in positionCounts.keys():
                    battingStats[playerID][positionCounts[row[0]]] = row[1]

            sql = '''SELECT SUM(IFNULL(b_H, 0))/SUM(IFNULL(b_AB, 0)) AS BA, 
            
                     SUM(IFNULL(b_BB, 0)) AS BB,
            
                     SUM((IFNULL(b_H, 0) + IFNULL(b_BB, 0) + IFNULL(b_HBP, 0)))/
                     SUM((IFNULL(b_AB, 0) + IFNULL(b_BB, 0) + IFNULL(b_HBP, 0) + IFNULL(b_SF, 0))) AS OBP, 
                     
                     SUM(((IFNULL(b_H, 0) - IFNULL(b_2B, 0) - IFNULL(b_3B, 0) - IFNULL(b_HR, 0)) + (2 * IFNULL(b_2B, 0)) + 
                     (3 * IFNULL(b_3B, 0)) + (4 * IFNULL(b_HR, 0)))) / SUM(IFNULL(b_AB, 0)) AS SLG
                 FROM batting
                 WHERE playerid=%s AND yearId=%s AND teamID=%s
                    AND b_R IS NOT NULL
                 '''
            # print(sql % (playerID, chosenYear, chosenTeamID))
            cur.execute(sql, [playerID, chosenYear, chosenTeamID])

            last3Stats = cur.fetchall()

            if len(last3Stats) == 0:
                # print(playerID)
                toDelete.append(playerID)
            for row in last3Stats:
                for col in row:
                    battingStats[playerID].append(col)

            i = 0
            delete_player = True
            for stat in battingStats[playerID]:
                if not delete_player or not str(stat).isnumeric() or i < 2:
                    i += 1
                    continue
                if stat != 0 and stat is not None:
                    # print(playerID + ' ' + str(stat))
                    delete_player = False


            if delete_player and playerID not in toDelete:
                toDelete.append(playerID)
            playerIDs.append(playerID)

        for playerID in playerIDs:
            if playerID in pitchingStats.keys():
                if pitchingStats[playerID][1] == 0:
                    del pitchingStats[playerID]

        for playerID in toDelete:
            if playerID in battingStats.keys():
                del battingStats[playerID]

        # print( pitchingStats )

    except Exception:
        con.rollback()
        print("Database Exception.")
        raise
    else:
        con.commit()

    
    # ---- Machine Learning Prediction ---- #

    team_stats = []
    stat_names = [ 'yearID', 'team_H', 'team_BB', 'team_BBA', 'team_HBP',
                   'team_AB', 'team_SF', 'team_R', 'team_2B', 
                   'team_3B', 'team_HR', 'team_IPouts', 'team_SO', 
                   'team_W_Per' ]

    try:
        cur = con.cursor()
        sql = '''SELECT yearID, team_H, team_BB, team_BBA, team_HBP, 
                 team_AB, team_SF, team_R, team_2B, team_3B, 
                 team_HR, team_IPouts, team_SO, team_W / team_G * 100 AS team_W_Per
                 FROM teams 
                 WHERE team_name = %s AND yearID BETWEEN %s AND %s 
                 ORDER BY yearID'''

        cur.execute( sql, [chosenTeam, chosenYear-20, chosenYear] )
        stats = cur.fetchall()


        for row in stats:
            team_stat = []
            for i in range( 0, len(row) ):
                team_stat.append( row[i] )
            team_stats.append( team_stat )

    except Exception:
        con.rollback()
        print("Database Exception.")
        raise
    else:
        con.commit()

    if( len( team_stats ) < 20 ):
         return render_template('stats.html', title='Stats', chosenTeam=chosenTeam, chosenYear=chosenYear, roster=rosterList,
                           battingStats=battingStats, pitching_data=pitchingStats, curr_year=chosenYear)
	
    df = pd.DataFrame( team_stats, columns = stat_names )
    print(df)
    print()

    OBP = ( df['team_H'] + df['team_BB'] + df['team_HBP'] ) / ( df['team_AB'] + df['team_BB'] + df['team_HBP'] + df['team_SF'] )
    SLG = ( df['team_H'] - df['team_2B'] - df['team_3B'] - df['team_HR'] + 2*df['team_2B'] + 3*df['team_3B'] + 4*df['team_HR'] ) / df['team_AB']
    WHIP = ( df['team_H'] + df['team_BBA'] ) / ( df['team_IPouts']/3 )
    Kper9 = ( df['team_SO'] / ( df['team_IPouts'] / 3 ) )

    derivedDf = pd.DataFrame( { 'yearID' : df['yearID'], 'OBP' : OBP, 'SLG' : SLG, 'WHIP': WHIP, 'Kper9' : Kper9 } )

    derivedDf['team_W_Per'] = df['team_W_Per']
    
    df = derivedDf
    print(df)
    currTeam = df.iloc[-1]
    df = df.iloc[:-1 , :]
    df = df.dropna().reset_index(drop=True)


    features = ['OBP', 'SLG', 'WHIP', 'Kper9']
    X = np.array( df[ features ] )
    y = np.array( df[ 'team_W_Per' ] )


    currTeamStats = [ currTeam['OBP'], currTeam['SLG'], currTeam['WHIP'], currTeam['Kper9'] ]
    try:
    	reg = LinearRegression().fit(X, y)
    	prediction = reg.predict( np.array( [currTeamStats] ))
    except Exception:
    	return render_template('stats.html', title='Stats', chosenTeam=chosenTeam, chosenYear=chosenYear, roster=rosterList,
			       battingStats=battingStats, pitching_data=pitchingStats, message="none found" ) 
			       

    kf = KFold(n_splits=5)
    RMSEs = []

    for i, (train_index, test_index) in enumerate( kf.split(X) ):
        X_train = X[train_index]
        X_test = X[test_index]
        y_train = y[train_index]
        y_test = y[test_index]

        model = LinearRegression()
        model = model.fit( X_train, y_train )
        y_pred = model.predict(X_test)
        #y_pred = np.round(y_pred, 0)
        mse = mean_squared_error( y_test, y_pred )

        #print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

        RMSEs.append( round(mse, 2) )

    print("Cross Validation RMSE Scores for: " + str(chosenTeam) + " in " + str(chosenYear))
    print(RMSEs)

    # ---- End Machine Learning Section --- #

    
    return render_template('stats.html', title='Stats', chosenTeam=chosenTeam, chosenYear=chosenYear, roster=rosterList,
                           battingStats=battingStats, pitching_data=pitchingStats, prediction=round(prediction[0], 2),
                           actual=round(currTeam['team_W_Per'],2), curr_year=chosenYear)

#change 2.
        
@app.route('/admin')
@login_required
def admin():
    con = pymysql.connect(host=cfig.con['host'], user=cfig.con['user'], password=cfig.con['password'],
                      database=cfig.con['database'])
    id = current_user.username
    if id == "test1":
        cur = con.cursor()
        sql = ''' select * from users ;'''
        cur.execute(sql)     
        results = cur.fetchall()
        cur.close()        
        return render_template("admin.html", title='Admin', results=results)
    else:           
        flash("sorry you are not the admin bro!!!")
        return redirect(url_for('login'))

