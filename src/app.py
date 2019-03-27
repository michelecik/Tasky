from flask import Flask, render_template, request, session
import json
import sys

from lib.dbconnection import *
from lib.authentication import *

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

dbConn = getConnection()

@app.route("/")
def main():
    # Test user is logged
    #if (getUsrId(dbConn, session.get('userid'), session.get('psw'))['code'] == 200):
        #return home()
    return login()

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
        else:
            return json.dumps(response)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if ((request.method == 'GET')):
        return render_template('signup.html')
    else:
        data = json.loads(request.get_data())

        createUser(dbConn, data)

        response = getUsrId(dbConn, data['userid'], data['psw'])

    return json.dumps(response)


# ---- MAIN ---- #
if __name__ == "__main__":
    app.run()