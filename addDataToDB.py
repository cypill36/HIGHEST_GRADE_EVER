import pymysql
import csi3335 as cfg

con = pymysql.connect(host     = cfg.mysql['location'], 
                      user     = cfg.mysql['user'], 
                      password = cfg.mysql['password'], 
                      database = cfg.mysql['database'])

try:
    cur = con.cursor()
    sql = '''SELECT * FROM batting 
             '''
    cur.execute(sql)
    
    column_names = [i[0] for i in cur.description]

    for d in cur.description:
        print(d)

    #print(column_names)

except Exception:
    con.rollback()
    print("Database Exception.")
    raise
else:
    con.commit()
finally:
    con.close()




