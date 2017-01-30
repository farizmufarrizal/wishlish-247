import sqlite3 as lite
import sys

con = lite.connect('test.db')
cur = con.cursor()

sql="""
DELETE FROM Cars
WHERE id = 13
"""

with con:
  cur.execute(sql)
