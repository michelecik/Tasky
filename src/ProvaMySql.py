from mysql import connector
from flask import Flask, render_template, request
import json
import sys

app = Flask(__name__, static_url_path='/static')

mySQL_db = connector.connect(
  host="localhost",
  user="user",
  passwd="CiaoCiao88",
  database="formazione_python"
)
mySQL_cursor = mySQL_db.cursor(dictionary=True)

def checkUsr(usr, psw):
    try:
        sql = "SELECT id FROM users WHERE userid = '{}' AND psw_MD5 = '{}'".format(usr, psw)
        mySQL_cursor.execute(sql)
        result = mySQL_cursor.fetchall()

        if len(result) <= 0:
            response = {
                'code': 403,
                'content': 'User o Password errate'
            }
            return response

        for tupla in result:
            id = tupla['id']
    except:
        response = {
            'code': 500,
            'content': 'Errore anomalo'
        }
        return response

    response = {
        'code': 200,
        'content': 'L\'utente esiste',
        'id': id
    }

    return response

@app.route("/")
def main():
    return render_template('home.html')

@app.route('/signIn')
def signIn():
    return render_template('signin.html')

@app.route('/signUp')
def signUp():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.get_data())

    # get information
    userid = data['userid']
    psw = data['psw']
    email = data['email']
    tel = data['tel']
    name = data['name']
    surname = data['surname']
    # verifico che l'utente non esista già
    try:
        sql = "SELECT id FROM users WHERE userid = '{}'".format(userid)
        mySQL_cursor.execute(sql)
        result = mySQL_cursor.fetchall()

        if len(result) > 0:
            response = {
                'code': 409,
                'content': 'L\'utente è gia esistente'
            }
            return json.dumps(response)
    except:
        response = {
            'code': 500,
            'content': 'Errore anomalo'
        }
        return json.dumps(response)

    # inserisco l'utente nel DB
    try:
        sql = "INSERT INTO users (userid, psw_MD5, email, tel, nome, cognome) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (userid, psw, email, tel, name, surname)
        mySQL_cursor.execute(sql, val)
        mySQL_db.commit()
    except:
        response = {
            'code': 500,
            'content': ('Errore durante l\'inserimento della query: ',sys.exc_info()[0])
        }
        return json.dumps(response)


    response = {
        'code': 200,
        'content': 'Utente creato con successo'
    }
    return json.dumps(response)

@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())

    # get information
    userid = data['userid']
    psw = data['psw']

    response = checkUsr(userid, psw)

    return json.dumps(response)

@app.route('/getUserInfo', methods=['POST'])
def getUserInfo():
    data = json.loads(request.get_data())

    # get information
    userid = data['userid']
    psw = data['psw']

    response_TMP = checkUsr(userid, psw)

    if response_TMP['code'] == 200:
        id = response_TMP['id']
        response = dict()
        try:
            sql = "SELECT nome, cognome, email, tel FROM users WHERE id={}".format(id)
            mySQL_cursor.execute(sql)
            result = mySQL_cursor.fetchall()

            if len(result) <= 0:
                response = {
                    'code': 403,
                    'content': 'User o Password errate'
                }
                return json.dumps(response)

            response['code'] = 200
            for tupla in result:
                response['nome'] = tupla['nome']
                response['cognome'] = tupla['cognome']
                response['tel'] = tupla['tel']
                response['email'] = tupla['email']
        except:
            response = {
                'code': 500,
                'content': 'Errore anomalo'
            }

    return json.dumps(response)

@app.route('/getAllMessage', methods=['POST'])
def getAllMessage():
    data = json.loads(request.get_data())

    # get information
    userid = data['userid']
    psw = data['psw']

    response_TMP = checkUsr(userid, psw)

    if response_TMP['code'] == 200:
        response = dict()
        try:
            sql = "SELECT c.title AS title, c.message AS message, u.userid AS userid FROM users u JOIN comments c ON u.id = c.FK_user"
            mySQL_cursor.execute(sql)
            result = mySQL_cursor.fetchall()

            if len(result) <= 0:
                response = {
                    'code': 200
                }
                return json.dumps(response)

            response['code'] = 200
            response['comments'] = list()
            for tupla in result:
                comment_tmp = {
                    'title': tupla['title'],
                    'message': tupla['message'],
                    'author': tupla['userid']
                }
                response['comments'].append(comment_tmp)
        except:
            response = {
                'code': 500,
                'content': 'Errore anomalo'
            }
    else:
        return json.dumps(response_TMP)

    return json.dumps(response)

# ---- MAIN ---- #
if __name__ == "__main__":
    app.run()