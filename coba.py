import sqlite3 as lite
from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route("/")
def main():
    #return "Welcome!"
    return render_template('index.html')

@app.route("/asik")
def asik():
    con = lite.connect("test.db")
    con.row_factory=lite.Row

    cur = con.cursor()
    cur.execute("select * from Cars")

    rows = cur.fetchall();
    con.close()
    return render_template('asik.html',rows = rows)
if __name__ == "__main__":
    app.run(debug="True")
