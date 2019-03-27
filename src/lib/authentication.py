from  model.Tables import *
def getUsrId(dbConn, usr, psw):
    try:
        result = dbConn.s.query(Utenti.id).filter(Utenti.userid == usr, Utenti.psw_MD5 == psw).first()

        if not (result): # Credenziali errate
            response = {
                'code': 403,
                'content': 'User o Password errate'
            }
            return response

    except Exception as e:
        print(e)
        response = {
            'code': 500,
            'content': 'Errore anomalo'
        }
        return response

    response = {
        'code': 200,
        'content': 'L\'utente esiste',
        'id': result.id
    }

    return response

def createUser(dbConn, userData):
    # Controlli di validità
    # ...
    user_tmp = Utenti(userData)

    user_validate = user_tmp.validate()

    if (getUsrId(dbConn, userData['userid'], userData['psw'])['code'] == 200):
        user_validate['userid'] = 'Il nome utente è gia presente'

    len(user_validate)
    if (len(user_validate)>0):
        response = {
            'code': 400,
            'content': 'Dati invalidi',
            'msg': user_validate
        }
        return response

    try:
        dbConn.s.add(user_tmp)
        dbConn.s.commit()
    except Exception as e:
        print(e)
        response = {
            'code': 500,
            'content': 'Errore anomalo'
        }
        return response

    response = {
        'code': 200,
        'content': 'Utente creato correttamente'
    }

    return response