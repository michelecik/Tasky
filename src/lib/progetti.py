from lib.dbconnection import *
from lib.authentication import *
from model.Tables import Progetti, Fasi

import traceback



def getAllProgetti(dbConn, session):
    userId = getUsrId(dbConn, session.get('userid'), session.get('psw'))['id']
    res = dbConn.s.query(Progetti).filter(Progetti.fk_utente == userId).all()
    return res


def getUserPermissionProject(dbConn, userId, projectId):
    try:
        result = dbConn.s.query(Progetti).filter(Progetti.id == projectId, Progetti.fk_utente == userId).first()

        if not (result):
            response = {
                'code': 403,
                'content': 'Non si dispone dei permessi necessari per accedere al progetto'
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
        'content': 'L\'utente è abilitato ad accedere al progetto ' + result.codice + ': ' + result.nome
    }

    return response

def getFasiProgetto(dbConn, projectId):

    prova = dict()
    def getChildren(fasi, children):
        fasi_tmp = dict()
        for index in children:
            child = fasi[index]
            fasi_tmp[index] = dict()
            fasi_tmp[index]['info'] = child['info']
            fasi_tmp[index]['children'] = dict()
            if (len(child['children'])>0):
                fasi_tmp[index]['children'] = getChildren(fasi, child['children'])
            else:
                fasi_tmp[index]['children'] = None

        return fasi_tmp

    try:
        result = dbConn.s.query(Fasi).filter(Fasi.FK_progetto == projectId).all()

        fasi_tmp = dict()
        for tupla in result:
            fasi_tmp[tupla.id] = dict()
            fasi_tmp[tupla.id]['info'] = tupla.toDict()
            fasi_tmp[tupla.id]['children'] = list()

        top_level = list()
        for tupla in result:
            if (tupla.parent):
                fasi_tmp[tupla.parent]['children'].append(tupla.id)
            else:
                top_level.append(tupla.id)

        fasi = dict()
        for i in top_level:
            fase = fasi_tmp[i]
            fasi[i] = dict()
            fasi[i]['info'] = fase['info']
            fasi[i]['children'] = getChildren(fasi_tmp, fase['children'])
    except Exception as e:
        print('-------------------- ERRORE --------------------------------')
        #print('ERRORE', e)
        print(traceback.print_exc())
        response = {
            'code': 500,
            'content': 'Errore anomalo'
        }
        return response

    response = {
        'code': 200,
        'content': '',
        'fasi': fasi
    }

    return response

def getProgettoById(dbConn, session, project_id):
    res = dbConn.s.query(Progetti).filter(Progetti.id == project_id).first()
    return res

def getProgettoById(dbConn, session, project_id):
    res = dbConn.s.query(Progetti).filter(Progetti.id == project_id).first()
    return res

def getProgettoById(dbConn, session, project_id):
    res = dbConn.s.query(Progetti).filter(Progetti.id == project_id).first()
    return res
