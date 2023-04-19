import pymysql
import csi3335 as cfg

inFile = open("./CSVfiles/ModifiedFranchises.csv")

con = pymysql.connect(host=cfg.mysql['location'],
                      user=cfg.mysql['user'],
                      password=cfg.mysql['password'],
                      database=cfg.mysql['database'])

try:

    cur = con.cursor()

    sql = '''SELECT * FROM franchises '''
    cur.execute(sql)

    column_names = [i[0] for i in cur.description]

    sql = '''INSERT INTO franchises ( '''

    for c in column_names:
        sql += c + ", "

    sql = sql[:-2]
    sql += ") VALUES( %s )"

    inFile.readline()
    while lines := inFile.readline():

        values = ""
        lines.strip(",\n\t ")
        splitLine = lines.split(",")
        for s in splitLine:
            s.strip("\n\t ")
            values += s + ", "

        print(sql)
        print(values)
        cur.execute(sql, values[:-2])


except Exception:
    con.rollback()
    print("Database Exception.")
    raise
else:
    con.commit()
finally:
    con.close()

inFile.close()
