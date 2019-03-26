from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Clienti(Base):
    __tablename__ = 'clienti'

    def __init__(self):
        self.id = Column(Integer, primary_key=True)
        self.ragione_sociale = Column(String)
        self.piva = Column(String)
        self.cf = Column(String)


class Commissioni(Base):
    __tablename__ = 'commissioni'

    def __init__(self):
        self.FK_progetto = Column(Integer, primary_key=True)
        self.FK_cliente = Column(Integer, primary_key=True)


class Fasi(Base):
    __tablename__ = 'fasi'

    def __init__(self):
        self.id = Column(Integer, primary_key=True)
        self.nome = Column(String)
        self.descrizione = Column(String)
        self.data_inizio = Column(Date)
        self.data_fine = Column(Date)
        self.parent = Column(Integer)
        self.isMain = Column(Integer)
        self.FK_progetto = Column(Integer)
        self.FK_stato = Column(Integer)


class Incarichi(Base):
    __tablename__ = 'incarichi'

    def __init__(self):
        self.FK_fase = Column(Integer, primary_key=True)
        self.FK_utente = Column(Integer, primary_key=True)
        self.FK_ruolo = Column(Integer, primary_key=True)


class Progetti(Base):
    __tablename__ = 'progetti'

    def __init__(self):
        self.id = Column(Integer, primary_key=True)
        self.nome = Column(String)
        self.codice = Column(String)
        self.descrizione = Column(String)


class Ruoli(Base):
    __tablename__ = 'ruoli'

    def __init__(self):
        self.id = Column(Integer, primary_key=True)
        self.nome = Column(String)
        self.canModify = Column(Integer)


class Stati(Base):
    __tablename__ = 'stati'

    def __init__(self):
        self.id = Column(Integer, primary_key=True)
        self.nome = Column(String)
        self.descrizione = Column(String)
        self.colore = Column(String)


class Utenti(Base):
    __tablename__ = 'utenti'

    def __init__(self):
        self.id = Column(Integer, primary_key=True)
        self.userid = Column(String)
        self.psw_MD5 = Column(String)
        self.email = Column(String)
        self.tel = Column(String)
        self.nome = Column(String)
        self.cognome = Column(String)