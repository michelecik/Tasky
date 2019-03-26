import sqlalchemy as db
class Database:

    def __init__(self, engine): # "engine" è l'oggetto sqlalchemy.create_engine() da dbconection.py
        self.engine = engine
        self.db = db
        self.connection = engine.connect()

        metadata = db.MetaData()

        self.clienti = db.Table('clienti', metadata, autoload=True, autoload_with=engine)
        self.commissioni = db.Table('commissioni', metadata, autoload=True, autoload_with=engine)
        self.fasi = db.Table('fasi', metadata, autoload=True, autoload_with=engine)
        self.incarichi = db.Table('incarichi', metadata, autoload=True, autoload_with=engine)
        self.progetti = db.Table('progetti', metadata, autoload=True, autoload_with=engine)
        self.ruoli = db.Table('ruoli', metadata, autoload=True, autoload_with=engine)
        self.stati = db.Table('stati', metadata, autoload=True, autoload_with=engine)
        self.utenti = db.Table('utenti', metadata, autoload=True, autoload_with=engine)
