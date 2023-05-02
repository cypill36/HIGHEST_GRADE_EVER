# Team: Highest Grade Ever
Members: Yaseen Arab, Alex Kubicek, Kaylynn Beard, Cyril Pillai

Database Design and Application Final Project

How to Access Website: ...
```
```

Admin Login:



How to Update Database to Match our Updated Database:
```
\. createTables.sql
python renameIDs.py
python add2022Data.py (warning: this could take up to 10 minutes to run!)
```


Imported Python Modules:
pymysql
flask
...

What We Did:

- Updated database with all new/updated 2022 data (add2022Data.py)
- Renamed all ID attributes to a unique name (renameIDs.py)
- Add user table and log table to database (createTables.sql)
- Machine learning... (extra credit)

from the website...
- Add user support to the database. This should include (at a minimum) a user name and encrypted password.
- Create a web/database app that requires users to login into the system. Login information must be secure.
- Once logged in, the user may provide a team name and a year. This should be input from a drop down menu requesting the team name, and then a drop down menu with the valid years. The system will log the selections made by a user.
- Write a web page to display the roster for the team submitted. Batting and pitching statistics should be separate. For each batter, include the number of games played at each position and his ''slash line,'' consisiting of his batting average, on base percentage and slugging percentage. For each pitcher, include the number of games pitched, the number of games started, the innings pitched (not IPOuts), the WHIP and the strikeouts per 9 innings.
- Have an admin user (password should be included in your readme file). The admin user can see the logged information for each user and the total requests for all users.

