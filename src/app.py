from flask import Flask, render_template, request, session, redirect, flash
import json
import os

from lib.dbconnection import *
from lib.authentication import *
from lib.progetti import *


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = os.urandom(24)

dbConn = getConnection() # Connessione con il DB (la funzione getConnection è in lib/dbconnection.py

@app.route("/")
def main():
    # Test user is logged
    if (getUsrId(dbConn, session.get('userid'), session.get('psw'))['code'] == 200):
        print('USER IS LOGGED')
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

    return redirect('/overview')



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


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    clicked = None
    if request.method == 'POST':
        print('GOT POST REQUESTTTTTTTTTTT')
        clicked = json.loads(request.get_data())
        print(clicked['id'], clicked['titolo'])
        progetto = getProgettoById(dbConn, session, clicked['id'])
        progetto.stato = 0
        dbConn.s.commit()
        flash('progetto elimineto')

    return redirect('/overview')

@app.route('/overview')
def overview():
    if (getUsrId(dbConn, session.get('userid'), session.get('psw'))['code'] == 200):
        return render_template('overview.html', progetti = getAllProgettiAttivi(dbConn, session) )
    else:
        return redirect('/login')


@app.route('/project',  methods=['GET'])
def project():
    projectId = request.args.get('id', default=None, type=int)

    response = getUsrId(dbConn, session.get('userid'), session.get('psw'))
    if (response['code'] == 200):
        userId = response['id']

        if not (projectId):
            return redirect('overview')

        response = getUserPermissionProject(dbConn, userId, projectId)

        if (response['code'] == 200):
            response = getFasiProgetto(dbConn, projectId)
            if (response['code'] == 200):
                stati = getStatiProgetti(dbConn)
                print('------------------------------------------------------ STATI: ', stati)
                return render_template('project.html', fasi = json.dumps(response['fasi']), stati = json.dumps(stati['stati']))
        else:
            return overview()
    else:
        return redirect('login')

    return render_template('overview.html', progetti = getAllProgetti(dbConn, session) )


@app.route('/editFase', methods=['POST'])
def editFase():
    print('-------------------------------- editFase ----------------------------------------')
    response = getUsrId(dbConn, session.get('userid'), session.get('psw'))
    if (response['code'] == 200):
        if request.method == 'POST':
            print(request.form)
            if request.form['id']:
                fase = getFaseById(dbConn, request.form['id'])
                fase.nome = request.form['nome'].strip()
                fase.descrizione = request.form['descrizione'].strip()
                fase.data_inizio = request.form['data_inizio'].strip()
                fase.data_fine = request.form['data_fine'].strip()
                fase.parent = request.form['parent'].strip()
                if len(request.form['parent'].strip()) <= 0:
                    fase.parent = None
                else:
                    fase.parent = request.form['parent'].strip()
                fase.FK_progetto = request.form['FK_progetto'].strip()
                fase.FK_stato = request.form['FK_stato'].strip()

                try:
                    dbConn.s.commit()
                except Exception as e:
                    response = {
                        'code': 500,
                        'content': 'Errore anomalo'
                    }

                return redirect('/project?id=' + request.form['FK_progetto'])
            else:
                faseData = dict()
                faseData['nome'] = request.form['nome']
                faseData['descrizione'] = request.form['descrizione']
                faseData['FK_stato'] = request.form['FK_stato']
                faseData['data_inizio'] = request.form['data_inizio']
                faseData['data_fine'] = request.form['data_fine']
                faseData['FK_progetto'] = request.form['FK_progetto']
                faseData['parent'] = request.form['parent']
                try:
                    fase = Fasi(faseData['nome'], faseData['descrizione'], faseData['data_inizio'], faseData['data_fine'], faseData['parent'], 0, faseData['FK_progetto'], faseData['FK_stato'])

                    dbConn.s.add(fase)
                    dbConn.s.commit()

                    return redirect('/project?id=' + request.form['FK_progetto'])
                except Exception as e:
                    response = {
                        'code': 500,
                        'content': 'Errore anomalo'
                    }
            return redirect('overview')

        return redirect('overview')
    else:
        return redirect('login')

# ---- MAIN ---- #
if __name__ == "__main__":
    app.run()