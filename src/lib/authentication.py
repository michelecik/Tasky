def getUsrId(dbConn, usr, psw):
    try:
        #sql = "SELECT id FROM users WHERE userid = '{}' AND psw_MD5 = '{}'".format(usr, psw)
        sql = dbConn.db.select([dbConn.utenti]).where(dbConn.db.and_(dbConn.utenti.columns.userid == usr, dbConn.utenti.columns.psw_MD5 == psw))
        query_stack = dbConn.engine.execute(sql)
        result = query_stack.fetchall()

        print(result)

        if len(result) <= 0:
            response = {
                'code': 403,
                'content': 'User o Password errate'
            }
            return response

        #for tupla in result:
            #id = tupla['id']
    except:
        response = {
            'code': 500,
            'content': 'Errore anomalo'
        }
        return response

    response = {
        'code': 200,
        'content': 'L\'utente esiste'#,
        #'id': id
    }

    return response