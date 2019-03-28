from flask import Flask, render_template, request, session, redirect, flash
import json

from lib.dbconnection import *
from lib.authentication import *
from lib.progetti import *
from lib.fasi import *


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
    # Aggiunto nuovo commento
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
        projectStartDate = request.form['startDate']
        projectEndDate = request.form['endDate']

        userId = getUsrId(dbConn, session.get('userid'), session.get('psw'))['id']

        newProject = Progetti(projectName, projectCode, projectDesc, projectStartDate, projectEndDate, userId)
        
        dbConn.s.add(newProject)
        dbConn.s.commit()

        print(newProject.id)

        flash('Progetto creato correttamente')

        """ dopo aver creato il progetto creo le 5 fasi principali """

        fasi = ['Avvio', 'Pianificazione', 'Esecuzione', 'Monitoraggio e Controllo', 'Conclusione']
        for fase in fasi:
            newFase = Fasi(fase, None, None, None, None, 1, newProject.id, 1 )
            dbConn.s.add(newFase)
            dbConn.s.commit()

    return render_template('create.html')


""" @app.route('/addfase/<int:project_id>', methods=['GET', 'POST'])
def addFase(project_id) {
    faseSecondaria = Fasi('fase secondaria', 'fase secondaria', None, None, 1, 0, newProject.id, 1)
        dbConn.s.add(faseSecondaria)
        dbConn.s.commit()
} """

@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit(project_id):
    progetto = getProgettoById(dbConn, session, project_id)
    if request.method == 'POST':
        projectName = request.form['name']
        projectCode = request.form['code']
        projectDesc = request.form['desc']
        projectStartDate = request.form['startDate']
        projectEndDate = request.form['endDate']

        """ update progetto """
        progetto.nome = projectName
        progetto.codice = projectCode
        progetto.descrizione = projectDesc
        dbConn.s.commit()
        flash('Progetto modificato correttamente')

        return redirect('/overview')

    
    return render_template('edit.html', progetto = progetto)


@app.route('/delete/<int:project_id>')
def delete(project_id):
    if request.method == 'POST':
        print(project_id)
        proj = getProgettoById(dbConn, session, project_id)
        dbConn.s.delete(proj)

    return redirect('/overview')

@app.route('/overview')
def overview():
    return render_template('overview.html', progetti = getAllProgetti(dbConn, session) )


@app.route('/project')
def viewProject():
    id = request.args.get('id')
    print(id)
    return render_template(
        'project.html',
        progetto = getProgettoById(dbConn, session, id)
        )

# ---- MAIN ---- #
if __name__ == "__main__":
    app.run()