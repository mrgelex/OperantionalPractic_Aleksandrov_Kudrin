import sqlite3 as sl
con = sl.connect('inter\Logs.db')
with con:
    con.execute("""INSERT INTO DEVICES (serial, IMEI, name, type) VALUES ('3350','98763453', 'test', 'standart')""")
    con.commit()