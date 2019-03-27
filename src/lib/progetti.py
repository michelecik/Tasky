from lib.dbconnection import *
from lib.authentication import *
from model.Tables import Progetti



def getAllProgetti(dbConn, session):
    userId = getUsrId(dbConn, session.get('userid'), session.get('psw'))['id']
    res = dbConn.s.query(Progetti).filter(Progetti.fk_utente == userId).all()
    return res