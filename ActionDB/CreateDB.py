import sqlite3 as sl
con = sl.connect('Logs.db')
with con:
    con.execute("""
        CREATE TABLE DEVICES (
            id_device INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            IMEI INTEGER,
            name TEXT,
            type TEXT
        );
    """)
    con.execute("""
        CREATE TABLE LOG_EVENT (
            id_log INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_device INTEGER REFERENCES DEVICES (id_device),
            date_local DATE,
            time_local TIME,
            status INTEGER,
            depth INTEGER,
            power INTEGER
        );
    """)
    con.execute("""
        CREATE TABLE LOG_TIME (
            id_log INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_device INTEGER REFERENCES DEVICES (id_device),
            date_local DATE,
            time_local TIME,
            status INTEGER,
            depth INTEGER,
            power INTEGER
        );
    """)
    con.commit()