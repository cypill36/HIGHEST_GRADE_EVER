import pymysql
import os
import csi3335 as cfg


def check_in_database():
    global column_names, splitLine, table_name, cur
    # search for entry in database
    sqlFind = "SELECT * FROM " + table_name + " WHERE "
    for c, s in zip(column_names, splitLine):
        if s == "NA" or s == "\n" or s == "":
            s = "NULL"
        s = s.strip()
        s = s.replace('\'', '\\\'')

        if s != "NULL":
            sqlFind += c
            sqlFind += " = "
            if not s.isnumeric():
                sqlFind += "'"
            sqlFind += s
            if not s.isnumeric():
                sqlFind += "'"
            sqlFind += " AND "

    cur.execute(sqlFind[:-4])
    result = cur.fetchall()
    in_database = False
    if len(result) > 0:
        in_database = True
    return in_database


def check_in_database_primary_keys():
    global column_names, splitLine, table_name, cur, keys
    sqlFind = "SELECT * FROM " + table_name + " WHERE "
    for c, s in zip(column_names, splitLine):
        if c in keys:
            if s == "NA" or s == "\n" or s == "":
                s = "NULL"
            s = s.strip()
            s = s.replace('\'', '\\\'')

            if s != "NULL":
                sqlFind += c
                sqlFind += " = "
                if not s.isnumeric():
                    sqlFind += "'"
                sqlFind += s
                if not s.isnumeric():
                    sqlFind += "'"
                sqlFind += " AND "
    cur.execute(sqlFind[:-4])
    result = cur.fetchall()
    in_database = False
    if len(result) > 0:
        in_database = True
    return in_database


def year_22():
    global has_year_id, splitLine
    if int(splitLine[has_year_id]) > 2021:
        return True
    return False


con = pymysql.connect(host=cfg.mysql['location'],
                      user=cfg.mysql['user'],
                      password=cfg.mysql['password'],
                      database=cfg.mysql['database'])

directory = "./CSVfiles"
tables = []

# inFile = open("./CSVfiles/ModifiedBatting.csv")

counter = 0

try:

    cur = con.cursor()

    # go through files
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            counter += 1
            inFile = open(f)
            table_name = (filename[9:].split(".")[0])
            sql = '''SELECT * FROM ''' + table_name
            cur.execute(sql)
            column_names = [i[0] for i in cur.description]

            sql = '''INSERT INTO ''' + table_name + ''' ( '''

            if column_names[0] == "ID":
                column_names.pop(0)

            primary_key_sql = "SHOW keys FROM " + table_name + " WHERE key_name='PRIMARY'"
            cur.execute(primary_key_sql)
            keys_results = cur.fetchall()
            keys = []

            for key in keys_results:
                new_key = key[4]
                if new_key.lower() != 'id':
                    keys.append(key[4])

            for c in column_names:
                sql += c + ", "

            sql = sql[:-2]
            sql += ") VALUES( %s )"
            prev_sql = sql

            has_year_id = -1
            if 'yearid'.casefold() in (name.casefold() for name in column_names):
                for string in column_names:
                    if string.lower() == 'yearid':
                        has_year_id = column_names.index(string)
                        break

            inFile.readline()
            while lines := inFile.readline():

                sql = prev_sql
                values = ""
                splitLine = lines.split(",")

                # check before inserting
                insert = update = False
                if (has_year_id != -1 and year_22()) or (has_year_id == -1 and not check_in_database()):
                    insert = True
                    if len(keys) > 0 and check_in_database_primary_keys():
                        sql = "UPDATE " + table_name + " SET %s WHERE "
                        update = True

                if insert:

                    for c, s in zip(column_names, splitLine):
                        print(c + " " + s)
                        if c not in keys or not update:
                            if update:
                                values += "`" + c + "`" + "="
                            if s == "NA" or s == "\n" or len(s) == 0:
                                s = "NULL"
                            s = s.strip()
                            print(s)
                            # s = s.replace('\'', '\\\'')
                            print(s)
                            if not s.isnumeric() and s != "NULL":
                                values += "'"
                            values += s
                            if not s.isnumeric() and s != "NULL":
                                values += "'"
                            values += ", "
                        else:
                            sql += "`" + c + "`" + "="
                            if s == "NA" or s == "\n" or len(s) == 0:
                                s = "NULL"
                            s = s.strip()
                            s = s.replace('\'', '\\\'')
                            if not s.isnumeric() and s != "NULL":
                                sql += "'"
                            sql += s
                            if not s.isnumeric() and s != "NULL":
                                sql += "'"
                            sql += ", "
                    values = values[:-2]
                    sql = sql[:-2]
                    print(repr(sql.replace("%s", "{}").format(values)))  #
                    cur.execute(sql, values)
            inFile.close()

except Exception:
    con.rollback()
    print("Database Exception.")
    raise
else:
    con.commit()
finally:
    con.close()

# inFile.close()
