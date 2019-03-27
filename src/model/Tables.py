from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Clienti(Base):
    __tablename__ = 'clienti'

    id = Column(Integer, primary_key=True)
    ragione_sociale = Column(String)
    piva = Column(String)
    cf = Column(String)


class Commissioni(Base):
    __tablename__ = 'commissioni'

    FK_progetto = Column(Integer, primary_key=True)
    FK_cliente = Column(Integer, primary_key=True)


class Fasi(Base):
    __tablename__ = 'fasi'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descrizione = Column(String)
    data_inizio = Column(Date)
    data_fine = Column(Date)
    parent = Column(Integer)
    isMain = Column(Integer)
    FK_progetto = Column(Integer)
    FK_stato = Column(Integer)


class Incarichi(Base):
    __tablename__ = 'incarichi'

    FK_fase = Column(Integer, primary_key=True)
    FK_utente = Column(Integer, primary_key=True)
    FK_ruolo = Column(Integer, primary_key=True)


class Progetti(Base):
    __tablename__ = 'progetti'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    codice = Column(String)
    descrizione = Column(String)


class Ruoli(Base):
    __tablename__ = 'ruoli'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    canModify = Column(Integer)


class Stati(Base):
    __tablename__ = 'stati'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descrizione = Column(String)
    colore = Column(String)


class Utenti(Base):
    __tablename__ = 'utenti'

    id = Column(Integer, primary_key=True)
    userid = Column(String)
    psw_MD5 = Column(String)
    email = Column(String)
    tel = Column(String)
    nome = Column(String)
    cognome = Column(String)

    def __init__(self, userData):
        self.userid = userData['userid']
        self.psw_MD5 = userData['psw']
        self.email = userData['email']
        self.tel = userData['tel']
        self.nome = userData['name']
        self.cognome = userData['surname']
