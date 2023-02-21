import time
from abc import ABC
from app import messages
from app.app import Client


class State(ABC):
    def __init__(self, app: Client):
        self.app = app


class InitState(State):
    def connect(self, host, port, name, listening_port):
        self.app.connect(host=host, port=port, name=name, listening_port=listening_port)


class IdleState(State):
    def run_game(self, world_id):
        new_message = messages.Message(title=messages.RUN_GAME,
                                       time=time.time(),
                                       content={"world_id": world_id},
                                       author=self.app.id,
                                       receiver="server")
        self.app.send_message(new_message)

    def get_world(self, world_id):
        new_message = messages.Message(title=messages.GET_WORLD,
                                       time=time.time(),
                                       content={},
                                       author=self.app.id,
                                       receiver="server")
        self.app.send_message(new_message)

    def create_world(self, world):
        new_message = messages.Message(title=messages.CREATE_WORLD,
                                       time=time.time(),
                                       content={"id": world.id,
                                                "type": world.type,
                                                "owner": world.owner,
                                                "private": world.private},
                                       author=self.app.id,
                                       receiver="server")
        self.app.send_message(new_message)


class GamingState(State):
    pass

