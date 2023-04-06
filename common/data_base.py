from sqlalchemy import create_engine, exc
import common.model as model
from common.model import *
postgres_url = 'postgresql://postgres:1133s1133@localhost/postgres'
game_url = 'postgresql://postgres:1133s1133@localhost/game'
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

