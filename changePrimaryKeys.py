import pymysql
import csi3335sp2023 as cfg

con = pymysql.connect(host=cfg.mysql['location'],
                      user=cfg.mysql['user'],
                      password=cfg.mysql['password'],
                      database=cfg.mysql['database'])

tables = []

try:
    cur = con.cursor()
    sql = "SHOW tables"
    cur.execute(sql)
    results = cur.fetchall()
    for t in results:
        tables.append(t[0])

    for t in tables:
        attributes = []
        sql = "DESCRIBE " + t
        cur.execute(sql)
        results = cur.fetchall()

        sql = "ALTER TABLE " + t + " DROP PRIMARY KEY, ADD PRIMARY KEY ("

        for r in results:
            # attributes.append(r[0])
            put = False
            if ('id' in r[0].lower() and r[0].lower() != 'id') and "gidp" not in r[0].lower():
                put = True
                if r[0].lower() == 'lgid' and (t.lower() != 'leagues' and t.lower() != 'teams'):
                    put = False
            if put:
                sql += r[0] + ", "
        # for a in attributes:
            # print(a)
            # allstarfull - primary(playerid, lgid, teamid, yearid, gameid) other(gamenum, GP, startingPos)
            # appearances - primary(playerid, yearid, teaimid)
            # awards - primary(awardid, yearid, playerid)
            # awardsshare - primary(awardid, yearid, playerid)
            # batting - primary(playerid, yearid, teamid)
            # battingpost - primary(playerid, yearid, teamid, round)
            # collegeplaying - primary(playerid, schoolid, yearid)
            # divisions - primary(divid)
            # fielding - primary(playerid, yearid, teamid)
            # fieldingpost - primary(playerid, yearid, teamid, round)
            # franchises - primary(franchid)
            # halloffame - primary(playerid, yearid, category)
            # homegames - primary(teamid, parkid, yearid)
            # leagues - primary(lgID)
            # managers - primary(playerid, yearid, teamid)
            # parks - primary(parkid)
            # people - primary(playerID)
            # pitching - primary(playerid, yearid, teamid)
            # pitchingpost - primary(playerid, yearid, teamid)
            # salaries - primary(playerid, yearid, teamid) other(lgid)
            # schools - primary(schoolid)
            # seriespost - primary(teamIDwinner, teamIDloser, yearID)
            # teams - primary(teamid, yearid, lgid, divid, franchid)
        sql = sql[:-2] + ')'
        print(sql)  # cur.execute(sql) TODO change to execute!

except Exception:
    con.rollback()
    print("Database Exception.")
    raise
else:
    con.commit()
finally:
    con.close()
