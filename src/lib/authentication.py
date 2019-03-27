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

    dbConn.s.add(user_tmp)
    dbConn.s.commit()