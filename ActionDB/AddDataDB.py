import sqlite3 as sl
con = sl.connect('Logs.db')
with con:
    con.execute("""INSERT INTO DEVICES (IMEI, name, type) VALUES ('1234567890', 'test', 'standart')""")
    con.commit()