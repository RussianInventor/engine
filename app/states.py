import time
from abc import ABC, abstractmethod
import messages
from common import model, game
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
            self.app.game = game.Game([message.autor], )
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
            world = model.World(message.content["id"])
            world.type = message.content["type"]
            world.owner = message.content["owner"]
            world.private = message.content["private"]
            with new_session() as session:
                session.add(world)
                session.commit()


class GamingState(State):
    def handle_messages(self):
        pass
