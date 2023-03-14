import time
from abc import ABC, abstractmethod
import messages
from common import model, game, world
from sqlalchemy.orm import Session
from server.data_base import engine
from sqlalchemy import and_, or_


def new_session():
    return Session(bind=engine, autocommit=True).begin()


class State(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def handle_messages(self):
        pass


class IdleState(State):
    def handle_messages(self):
        message = self.app.input_messages.get()
        if message.title == messages.RUN_GAME:
            with new_session() as session:
                self.app.game = game.Game([message.autor], world.World.from_db(session, message.content["world_id"]))
        if message.title == messages.GET_WORLD:
            with new_session() as session:
                q = session.query(model.World)
                q = q.filter(or_(model.World.private == False,
                                 model.World.owner == message.author))
                worlds = q.all()
                answer = messages.Message(title=messages.WORLD_LIST,
                                          time=time.time(),
                                          content={
                                              "worlds": [{c.name: i.__getattribute__(c.name) for c in i.__table__.c} for
                                                         i in worlds]},
                                          author="server",
                                          receiver=message.author)
                self.app.send_message(message.author, answer)
        if message.title == messages.CREATE_WORLD:
            new_world = model.World(message.content["id"])
            new_world.type = message.content["type"]
            new_world.owner = message.content["owner"]
            new_world.private = message.content["private"]
            with new_session() as session:
                session.add(new_world)
                session.commit()
            self.app.send_message(message.author)


class GamingState(State):
    def handle_messages(self):
        pass
