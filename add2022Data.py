import pymysql
import os
import csi3335sp2023 as cfg


def check_for_duplicate_primary_key(values, columns, table, cursor):
    cursor.execute("SHOW keys FROM " + table_name + " WHERE key_name='PRIMARY';")
    results = cursor.fetchall()
    # no primary key in table (should be impossible but might as well check...)
    if cursor.rowcount == 0:
        return False
    keyColumnName = results[0][4]

    # search for entry with matching primary key
    findKeySql = "SELECT COUNT(*) FROM " + table + " WHERE " + keyColumnName + " = %s;";
    keyValue = ""
    for c, v in zip(column_names, values):
        if c == keyColumnName:
            keyValue = v
    cursor.execute(findKeySql, keyValue)
    result = cursor.fetchall()
    # return false if no results, matching primary key not found
    return result[0][0] != 0


def check_in_database(values, columns, table, cur):
    # search for entry in database
    findSql = "SELECT COUNT(*) FROM " + table + " WHERE "
    params = []
    for c, v in zip(columns, values):
        if v is None:
            findSql += c + " IS NULL AND "
        else:
            findSql += c + " = %s AND "
            params.append(v)
    findSql = findSql[:-5]
    findSql += ";"
    cur.execute(findSql, params)
    result = cur.fetchall()
    # return false if no results, row not found
    return result[0][0] != 0




con = pymysql.connect(host=cfg.mysql['location'],
                      user=cfg.mysql['user'],
                      password=cfg.mysql['password'],
                      database=cfg.mysql['database'])

directory = "./CSVfiles"

try:
    cur = con.cursor()

    # go through files
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            table_name = (filename[9:].split(".")[0])
            table_name = table_name.lower()
   # f = "./CSVfiles/5modifiedAppearances.csv"
   # table_name = "appearances"
            print("Inserting 2022 data for " + table_name + "...")

            sql = "SELECT * FROM " + table_name
            cur.execute(sql)
            column_names = [i[0] for i in cur.description]

            # auto_increment attributes are not inserted manually
            if column_names[0] == table_name + "ID":
                column_names.pop(0)

            sql = "INSERT INTO " + table_name + " ("
            hasYearID = False
            index = 0
            yearIDIndex = -1
            for c in column_names:
                sql += c + ", "
                if c.lower() == "yearid":
                    hasYearID = True
                    yearIDIndex = index
                index += 1
            sql = sql[:-2]
            sql += ") VALUES("

            inFile = open(f)
            inFile.readline()  # ignore header
            while lines := inFile.readline():
                insertSql = sql
                splitLine = lines.split(",")
                valuesList = []

                # clean up the data and get values
                for s in splitLine:
                    s = s.strip()
                    insertSql += "%s, "
                    if s == "NA" or s == "\n" or len(s) == 0:
                        valuesList.append(None)
                    elif s.isnumeric():
                        valuesList.append(int(s))
                    else:
                        valuesList.append(s)
                insertSql = insertSql[:-2]
                insertSql += ");"

                # check if this row should be inserted, updated, or neither
                update = False
                insert = False

                # if yearID is 2022, insert new row
                if hasYearID and valuesList[yearIDIndex] is not None and valuesList[yearIDIndex] > 2021:
                    insert = True
                # if exact row is not already in database
                elif not check_in_database(valuesList, column_names, table_name, cur):
                    # if primary key already exists, the row just needs to be updated
                    if check_for_duplicate_primary_key(valuesList, column_names, table_name, cur):
                        update = True
                    else:
                        # insert new row that doesn't have yearID/yearID of 2022
                        insert = True

                if insert:
                 #   print(insertSql)
                  #  print(valuesList)
                    cur.execute(insertSql, valuesList)


except Exception:
    con.rollback()
    print("Database Exception.")
    raise
else:
    con.commit()
    print("2022 records successfully added to database!")
finally:
    con.close()
