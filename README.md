# HighestGradeEver Baseball Application
CSI 3335 Database Design and Application Final Project

### Members:
- Yaseen Arab
- Alex Kubicek
- KayLynn Beard
- Cyril Pillai

Admin Login Information:
```
username: test1
password: Baylor123
```

## Updates to the Database
- Renamed all ID attributes to a unique name (renameIDs.py)
- Updated the database with all new/updated 2022 data (add2022Data.py)
  - Includes new data with yearID=2022
  - Includes updating rows already in the database with values that have changed in 2022 (ex: death dates, changed names, etc.)
  - The following tables are entirely up-to-date:
    - Franchises
    - People, Managers
    - Teams
    - Parks
    - Allstarfull
    - Appearances
    - Batting, BattingPost
    - Pitching, PitchingPost
    - Fielding, FieldingPost
    - HomeGames
    - SeriesPost

## Web Features
- User login/signup with username and encrypted password
- Admin login can view users, user logs, and user total requests
- Select team name and year from drop down menu to view...
  - player roster
  - each player's batting statistics
  - each player's pitching statistics
- Linear regression to predict % wins for current year based on data from last 20 years (OB %, slug %, whip %, .....) ---------------------------
  - if insufficient data (ex: no SF calculated for the year), prediction is omitted
  - if team has not been active for the past 20 years, predicted is omitted
  - result is compared to actual % wins
  
## Installation
1. Create a new database called ```highestgradeever``` and run ```\. highestgradeever``` to initialize the updated database.
2. Update ```csi3335sp2023.py``` to contain your username and password.
3. Install all required python modules listed below into your virtual environment.

### Imported Python Modules:
- flask
- flask_sqlalchemy
- flask_login
- pymysql
- pandas
- numpy
- werkzeug
- flask-wtf
- flask-migrate
- sklearn
- ... (these are all that are listed on the website, remove what we didn't use) -------------------------------

## How to Update the Database
1. Run ```python renameIDs.py``` to rename ID attributes.
2. Run ```python add2022Data.py``` to update the database. (Warning: this can take about 5 minutes to run!)

## How to Run the Web Application
1. Navigate to the subdirectory `GroupProjectFlask/`
2. Run `flask run`
2. Access the web app at `http://localhost:/` ----------------------------
