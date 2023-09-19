from sqlalchemy import create_engine, exc
import common.model as model
from common.model import *
from sqlalchemy.orm import Session
from .config import Config

postgres_url = Config.db_url
game_url = Config.game_db_url
engine = create_engine(postgres_url)
try:
    connection = engine.connect()
    connection.execute('commit')
    connection.execute('create database game')
    connection.close()
except exc.ProgrammingError:
    pass
engine = create_engine(game_url)

model.Base.metadata.create_all(engine)


def new_session(expire_on_commit=True):
    ses = Session(bind=engine, autocommit=True, expire_on_commit=expire_on_commit)
    ses.begin()
    return ses
