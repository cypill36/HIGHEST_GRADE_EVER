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

    # iterate over tables
    for t in tables:
        attributes = []
        sql = "DESCRIBE " + t
        cur.execute(sql)
        results = cur.fetchall()
        firstRow = results[0]

        # if table has ID attribute
        if firstRow[0] == 'ID':
            uniqueID = t + "ID"
            # rename ID column to tableID
            sql = "ALTER TABLE " + t + " RENAME COLUMN ID TO " + uniqueID + ";"
            cur.execute(sql)

except Exception:
    con.rollback()
    print("Database Exception.")
    raise
else:
    con.commit()
finally:
    con.close()