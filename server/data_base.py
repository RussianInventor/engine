from typing import List

import sqlalchemy.exc
from sqlalchemy import create_engine, exc
from sqlalchemy.dialects.postgresql import insert
import common.model as model
from common.model import *
from sqlalchemy.orm import Session
from .config import Config
from contextlib import contextmanager

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


@contextmanager
def new_session(expire_on_commit=True):
    ses = Session(bind=engine, autocommit=True, expire_on_commit=expire_on_commit)
    ses.begin()
    yield ses
    try:
        ses.commit()
    except sqlalchemy.exc.InvalidRequestError:
        pass
    ses.expunge_all()
    ses.close()


def upsert(session: Session, objects: List[model.Base]):
    if not objects:
        return
    table = objects[0].__table__
    stmt = insert(table).values([{c.name: getattr(obj, c.name) for c in table.c} for obj in objects])

    update_cols = [c.name for c in table.c if c not in list(table.primary_key.columns)]

    stmt = stmt.on_conflict_do_update(
        index_elements=table.primary_key.columns,
        set_={k: getattr(stmt.excluded, k) for k in update_cols}
    )

    session.execute(stmt)
