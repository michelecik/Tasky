import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, engine): # "engine" è l'oggetto sqlalchemy.create_engine() da dbconection.py
        self.db = db
        self.engine = engine
        Session = sessionmaker(bind=engine)
        self.s = Session()
