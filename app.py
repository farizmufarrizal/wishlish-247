from __future__ import print_function
import sys
import sqlite3 as lite
from flask import Flask, render_template, url_for, redirect, request, session


app = Flask(__name__)

@app.route("/")
def main():

    if 'username' in session:
        username_session = session['username']

        con = lite.connect("test.db")
        con.row_factory=lite.Row

        cur = con.cursor()
        cur.execute("SELECT first_name, last_name FROM Users WHERE username=(?)", [username_session])

        rows = cur.fetchall();
        con.close()
        return render_template('home.html', rows = rows)

    return render_template('index.html')
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))


@app.route('/carlist')
def carlist():
    con = lite.connect("test.db")
    con.row_factory=lite.Row

    cur = con.cursor()
    cur.execute("select * from Cars")

    print(rows['username'], file=sys.stderr)
    rows = cur.fetchall();
    con.close()
    return render_template('carlist.html',rows = rows)

@app.route('/insertcar')
def insertcar():
    return render_template('insertcar.html')

@app.route('/savecar', methods=['GET' , 'POST'])
def savecar():
    if request.method == 'POST':
        idcar = request.form['idcar']
        namecar = request.form['namecar']
        pricecar = request.form['pricecar']

        con = lite.connect('test.db')

        with con:

            cur = con.cursor()
            cur.execute("INSERT INTO Cars VALUES(?, ?, ?)",(idcar,namecar,pricecar))
            con.commit()

    return redirect(url_for('carlist'))

@app.route('/updatecar')
def updatecar():
    con = lite.connect("test.db")
    con.row_factory=lite.Row

    cur = con.cursor()
    cur.execute("select * from Cars")

    rows = cur.fetchall();
    con.close()
    return render_template('updatecar.html',rows = rows)

@app.route('/saveupdate', methods=['GET' , 'POST'])
def saveupdate():
    if request.method == 'POST':
        idcar = request.form['idcar']
        namecar = request.form['namecar']
        pricecar = request.form['pricecar']

        idselect = request.form['idcar']

        con = lite.connect('test.db')
        cur = con.cursor()

        with con:
            cur.execute("UPDATE Cars SET id==?, Name=?, Price=? WHERE id=?",(idcar,namecar,pricecar,idselect))
            con.commit()

    return redirect(url_for('carlist'))

@app.route('/deletecar')
def deletecar():
        con = lite.connect("test.db")
        con.row_factory = lite.Row

        cur = con.cursor()
        cur.execute("select id from Cars")

        rows = cur.fetchall();
        con.close()
        return render_template("deletecar.html", rows = rows)

@app.route('/godelete', methods=['GET' , 'POST'])
def godelete():
    if request.method == 'POST':
        idcar = request.form['idselect']
        con = lite.connect('test.db')
        cur = con.cursor()


        with con:
            cur.execute("DELETE FROM Cars WHERE id=(?)",[idcar])
            con.commit()

        return redirect(url_for('carlist'))


#SIGN UP

@app.route('/signuplist')
def signuplist():
    con = lite.connect("test.db")
    con.row_factory=lite.Row

    cur = con.cursor()
    cur.execute("select * from Users")

    rows = cur.fetchall();
    con.close()
    return render_template('signuplist.html',rows = rows)

@app.route("/signup")
def signup():

    return render_template('signup.html')

@app.route('/saveuser', methods=['GET' , 'POST'])
def saveuser():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        con = lite.connect('test.db')

        with con:

            cur = con.cursor()
            cur.execute("INSERT INTO Users (first_name, last_name, gender, email, username, password) VALUES(?, ?, ?, ?, ?, ?)",(firstname,lastname,gender,email,username,password))
            con.commit()

    return redirect(url_for('signuplist'))



@app.route('/carlist_delete/<int:idcar>', methods=['GET' , 'POST'])
def carlist_delete(idcar):
    try:
        idcar = str(idcar)
        con = lite.connect('test.db')
        cur = con.cursor()


        with con:
            cur.execute("DELETE FROM Cars WHERE id=(?)",[idcar])
            con.commit()

        return redirect(url_for('carlist'))

    except:

        return redirect(url_for('carlist'))


#SIGN IN
@app.route("/signin")
def signin():

    return render_template('signin.html')

@app.route("/home")
def home():

    return render_template('home.html')

@app.route("/gosignin", methods=['GET','POST'])
def gosignin():
    error = ""
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']

        con = lite.connect('test.db')
        cur = con.cursor()


        cur.execute("SELECT COUNT(1) FROM Users WHERE username=(?)",[username_form])

        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM Users WHERE password=(?)",[password_form])
            for row in cur.fetchall():
                if password_form==row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('main'))
                else:
                    error = "Invalid Credential"
        else:
           error = "Invalid Credential"

        return render_template('signin.html', error=error)
app.secret_key = 'fariz'
if __name__ == "__main__":
    app.run(debug="True")
