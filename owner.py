import sqlite3 as lite
import sys

con = lite.connect('test.db')

with con:

    cur = con.cursor()
    cur.execute("CREATE TABLE owner(id INT, Name TEXT, Alamat TEXT, kode INT)")
    cur.execute("INSERT INTO owner VALUES(101,'M. Ali','Porong',1)")
    cur.execute("INSERT INTO owner VALUES(102,'Ach. Prayogi','Candi',4)")
    cur.execute("INSERT INTO owner VALUES(103,'Suhanto','Sidoarjo', 6)")
