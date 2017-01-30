import sqlite3 as lite
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/carlist')
def carlist():
   con = lite.connect("test.db")
   con.row_factory = lite.Row

   cur = con.cursor()
   cur.execute("select * from Cars where price >= 30000 ")

   rows = cur.fetchall();
   con.close()
   return render_template("carlist.html",rows = rows)

@app.route('/insertcar')
def insertcar():
    return render_template("insertcar.html")


@app.route('/savecar', methods=['GET', 'POST'])
def savecar():
    if request.method == 'POST':
        idcar = request.form['idcar']
        namecar= request.form['namecar']
        pricecar = request.form['pricecar']

        con = lite.connect('test.db')

        with con: #Function like commit
            cur = con.cursor()
            cur.execute("INSERT INTO Cars VALUES (?,?,?)",(idcar,namecar,pricecar) )
            con.commit()

    return redirect(url_for('carlist'))


@app.route('/hello')
def fungsi_hello():
    return "Hello"

if __name__ == "__main__":
    app.run(debug="True")
