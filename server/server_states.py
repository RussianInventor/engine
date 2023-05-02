import logging
from abc import ABC, abstractmethod
from common.app import messages
from common import model, game, world
from sqlalchemy.orm import Session
from common.data_base import engine
from sqlalchemy import or_
import uuid


def new_session():
    ses = Session(bind=engine, autocommit=True)
    ses.begin()
    return ses


class State(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def handle_messages(self, msg: messages.Message):
        pass


class IdleState(State):
    def handle_messages(self, msg: messages.Message):
        logging.info(f'handle message: {msg.title}: {msg.content}')
        if msg.title == messages.MessageType.RUN_GAME:
            with new_session() as session:
                self.app.game = game.Game([msg.author], world.World.from_db(session, msg.content["world_id"]))
        if msg.title == messages.MessageType.GET_WORLD:
            with new_session() as session:
                q = session.query(model.World)
                q = q.filter(or_(model.World.private == False,
                                 model.World.owner == msg.author))
                worlds = q.all()
                msg.answer(content={"worlds": [{c.name: i.__getattribute__(c.name) for c in i.__table__.c} for i in worlds]})
                # self.app.send_message(message.author, answer)
        if msg.title == messages.MessageType.CREATE_WORLD:
            new_world = model.World(str(uuid.uuid4()))
            new_world.type = msg.content["type"]
            new_world.owner = msg.content["owner"]
            new_world.private = msg.content["private"]
            with new_session() as session:
                session.add(new_world)
                session.commit()
            msg.answer(content={c.name: new_world.__getattribute__(c.name) for c in new_world.__table__.c})


class GamingState(State):
    def handle_messages(self, msg: messages.Message):
        pass
