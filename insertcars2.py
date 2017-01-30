import sqlite3 as lite
import sys

cars = (
    (9, 'suzuki', 52642),
    (10, 'honda', 57127),
    (11, 'nissan', 9000),
    (12, 'hyunday', 29000),
    (13, 'jailing', 350000),
)


con = lite.connect('test.db')

with con:

    cur = con.cursor()

    #cur.execute("DROP TABLE IF EXISTS Cars")
    #cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
    cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
