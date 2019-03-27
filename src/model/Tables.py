from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from re import fullmatch as rematch

def isValidEmail(email):
    if len(email) > 7:
        if rematch('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) != None:
            return True
    return False

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
    userid = Column(String, unique=True)
    psw_MD5 = Column(String)
    email = Column(String)
    tel = Column(String)
    nome = Column(String)
    cognome = Column(String)

    def __init__(self, userData):
        self.userid = userData['userid'].strip()
        self.psw_MD5 = userData['psw'].strip()
        self.email = userData['email'].strip()
        self.tel = userData['tel'].strip()
        self.nome = userData['nome'].strip()
        self.cognome = userData['cognome'].strip()

    def validate(self):
        errors = dict()

        #validate userid
        if (len(self.userid)<4) or not(rematch('^[a-zA-Z0-9_]*$', self.userid)):
            errors['userid'] = 'Il nome utente deve essere lungo alme 4 caratteri e non deve contenere numeri'

        #validate psw_MD5
        if (len(self.psw_MD5) < 32):
            errors['psw'] = 'La password deve essere un\'impronta digitale di tipo MD5'

        # validate email
        if not (isValidEmail(self.email)):
            errors['email'] = 'L\'indirizzo email non è valido'

        # validate tel
        if (self.tel != ''):
            if (len(self.tel)<8) or not (self.tel.isdigit()):
                errors['tel'] = 'Il numero di telefono non è valido'

        # validate nome
        if (len(self.nome) < 3) or not(rematch('^[a-zA-Z_]*$', self.nome)):
            errors['nome'] = 'Il nome deve essere lungo almeno 3 caretteri e non deve contenere nè caretteri speciali nè numeri'

        # validate cognome
        if (len(self.cognome) < 2) or not (rematch('^[a-zA-Z_]*$', self.cognome)):
            errors['cognome'] = 'Il cognome deve essere lungo almeno 2 caretteri e non deve contenere nè caretteri speciali nè numeri'

        return errors
