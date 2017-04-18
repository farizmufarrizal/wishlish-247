from flask.ext.mysqldb import MySQL
from flask import Flask, render_template, url_for, redirect, request, session
import netifaces as ni
import time
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='wishlist'

mysql = MySQL(app)
global alip
alip =""
ni.ifaddresses('lo')
alip = ni.ifaddresses('lo')[2][0]['addr']


@app.route('/')
def index():
    if 'username' in session:
        username_session = session['username']
        if session['level_akses'] == "1":
            return render_template('dashboard_admin.html',session_user_name=username_session, leve_akses=session['level_akses'])
        elif session['level_akses'] == "2":
            return render_template('dashboard.html', session_user_name=username_session, leve_akses=session['level_akses'])
        else:
            return render_template('index_mysql.html')
    else:
        return render_template('index_mysql.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_admin.html')

@app.route('/home')
def main():
    if 'username' in session:
        username_session = session['username']

        cur = mysql.connection.cursor()
    #
    #     cur.execute("SELECT username FROM loguser WHERE password=(%s)", [password_session])
        cur.execute("SELECT * FROM loguser")
        rows = cur.fetchall();

        return render_template('menu.html', rows = rows)

    #return render_template('index_mysql.html')


@app.route('/carlist')
def carlist():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Cars")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('carlist_mysql.html', rows = rows)

@app.route('/insertcar')
def insertcar():
    return render_template('insertcar_mysql.html')
@app.route('/savecar', methods=['GET' , 'POST'])
def savecar():
    if request.method == 'POST':
        Id = request.form['idcar']
        Name= request.form['namecar']
        Price = request.form['pricecar']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Cars VALUES(%s,%s,%s)",(Id,Name,Price))
        mysql.connection.commit()
        return redirect(url_for('carlist'))

@app.route('/updatecar')
def updatecar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Id FROM Cars")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('update_mysql.html', rows = rows)

@app.route('/saveupdate', methods=['GET' , 'POST'])
def saveupdate():
    if request.method == 'POST':
        Id = request.form['idcar']
        Name = request.form['namecar']
        Price = request.form['pricecar']

        idselect = request.form['idcar']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Cars SET Name=%s, Price=%s WHERE Id=%s",(Name,Price,Id))
        mysql.connection.commit()

    return redirect(url_for('carlist'))

@app.route('/delete')
def delete():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Id FROM Cars")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('delete_mysql.html', rows = rows)
@app.route('/godelete', methods=['GET' , 'POST'])
def godelete():
    if request.method == 'POST':
        Id = request.form['idcar']

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Cars WHERE Id=(%s)",[Id])
        mysql.connection.commit()
        return redirect(url_for('carlist'))

@app.route('/signuplist')
def signuplist():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('signuplist_mysql.html', rows = rows)
@app.route("/signup")
def signup():

    return render_template('signup_mysql.html')

@app.route('/saveuser', methods=['GET' , 'POST'])
def saveuser():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users (first_name, last_name, gender, email, username, password, level_akses) VALUES(%s,%s,%s,%s,%s,%s,%s)",(firstname,lastname,gender,email,username,password,"2"))
        mysql.connection.commit()

    return redirect(url_for('signuplist'))

# @app.route("/home")
# def index():
#

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/gosignin", methods=['GET','POST'])
def gosignin():
      if request.method == 'POST':
          username_form = request.form['username']
          password_form = request.form['password']

          cur = mysql.connection.cursor()
          cur.execute("SELECT COUNT(1) FROM Users WHERE username=(%s)",[username_form])

          if cur.fetchone()[0]:
              cur.execute("SELECT password, level_akses FROM Users WHERE username=(%s)",[username_form])
              for row in cur.fetchall():
                  if password_form==row[0]:
                      session['username'] = request.form['username']
                      session['level_akses'] = row[1]
                      skrg = time.time()

                      cur.execute("INSERT INTO loguser VALUES(%s,%s,%s,%s)",(username_form,alip,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(skrg)),"login"))
                      mysql.connection.commit()
                      return redirect(url_for('index'))
                  else:
                      error = "Invalid Credential"
          else:
             error = "Invalid Credential"

          return render_template('signin.html', error=error)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


app.secret_key = 'fariz'

if __name__ == "__main__":
    app.run(debug="True")
