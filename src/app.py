from flask import Flask, render_template, request, session, redirect
import json

from lib.dbconnection import *
from lib.authentication import *
from lib.progetti import *

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

dbConn = getConnection() # Connessione con il DB (la funzione getConnection è in lib/dbconnection.py

@app.route("/")
def main():
    # Test user is logged
    if (getUsrId(dbConn, session.get('userid'), session.get('psw'))['code'] == 200):
        return render_template('index.html')
    return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if ((request.method == 'GET')):
        return render_template('signin.html')
    else:
        data = json.loads(request.get_data())

        # get information
        userid = data['userid']
        psw = data['psw']

        response = getUsrId(dbConn, userid, psw)

        if (response['code'] == 200):
            session['userid'] = userid
            session['psw'] = psw
            #return main()

        return json.dumps(response)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if ((request.method == 'GET')):
        return render_template('signup.html')
    else:
        data = json.loads(request.get_data())

        response = createUser(dbConn, data)

        if (response['code'] == 200):
            response = getUsrId(dbConn, data['userid'], data['psw'])

        return json.dumps(response)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        projectName = request.form['name']
        projectCode = request.form['code']
        projectDesc = request.form['desc']
        userId = getUsrId(dbConn, session.get('userid'), session.get('psw'))['id']
        print(userId)

        newProject = Progetti(projectName, projectCode, projectDesc, userId)
        print(newProject)
        dbConn.s.add(newProject)
        dbConn.s.commit()

    return render_template('create.html')

@app.route('/overview')
def overview():
    return render_template('overview.html', progetti = getAllProgetti(dbConn, session) )

# ---- MAIN ---- #
if __name__ == "__main__":
    app.run()