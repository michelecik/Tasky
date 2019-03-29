# dbconnection.py
import time
import traceback

from sqlalchemy import create_engine, update
from sqlalchemy.exc import OperationalError
from model.Database import Database

from settings.constants import *


def getConnection():
    db = None
    for i in range(RETRIES):
        try:
            engine = create_engine("{}://{}:{}@{}:{}/{}".format(DATABASE_DRIVER,
                                                                DATABASE_USER_ROOT,
                                                                DATABASE_ROOT_PASSWORD,
                                                                DATABASE_HOST,
                                                                DATABASE_PORT,
                                                                DATABASE_NAME), echo=False)
            db = Database(engine)
        except OperationalError as ex:
            print(traceback.format_exc())
            time.sleep(WAITING_TIME)
        else:
            break
    else:
        raise ex

    return db

