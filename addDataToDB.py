import pymysql
import csi3335sp2023 as cfg

con = pymysql.connect(host=cfg.mysql['location'],
                      user=cfg.mysql['user'],
                      password=cfg.mysql['password'],
                      database=cfg.mysql['database'])

inFile = open("./CSVfiles/ModifiedBatting.csv")

try:
    cur = con.cursor()
    sql = '''SELECT * FROM batting'''
    cur.execute(sql)
    column_names = [i[0] for i in cur.description]

    sql = '''INSERT INTO batting ( '''

    if column_names[0] == "ID":
        column_names.pop(0)

    for c in column_names:
        sql += c + ", "

    sql = sql[:-2]
    print(sql)
    sql += ") VALUES( %s )"

    inFile.readline()
    while lines := inFile.readline():
        values = ""
        splitLine = lines.split(",")
        for s in splitLine:
            if s == "NA" or s == "\n":
                s = "NULL"
            s = s.strip()
            s = s.replace('\'', '\\\'')
            if not s.isnumeric() and s != "NULL":
                values += "'"
            values += s
            if not s.isnumeric() and s != "NULL":
                values += "'"
            values += ", "


        values = values[:-2]
        # search for entry in database
        sqlFind = "SELECT * FROM batting WHERE "
        for c, s in zip(column_names, splitLine):
            sqlFind += c;
            if s == "NA" or s == "\n" or s == "":
                s = "NULL"
            s = s.strip()
            s = s.replace('\'', '\\\'')

            if s == "NULL":
                sqlFind += " IS NULL"
            else:
                sqlFind += " = "
                if not s.isnumeric():
                    sqlFind += "'"
                sqlFind += s
                if not s.isnumeric():
                    sqlFind += "'"
            sqlFind += " AND "

        cur.execute(sqlFind[:-4])
        result = cur.fetchall()

        if len(result) == 0:
            print(sqlFind[:-4])
           # cur.execute(sql % values)

except Exception:
    con.rollback()
    print("Database Exception.")
    raise
else:
    con.commit()
finally:
    con.close()

inFile.close()
