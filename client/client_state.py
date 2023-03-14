import time
from abc import ABC
from app import messages
from app.app import Client

class State(ABC):
    def __init__(self, app: Client):
        self.app = app

    def execute(self, function_name, kwargs=None):
        if kwargs is None:
            kwargs = {}
        return getattr(self, function_name)(**kwargs)



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

    def get_world(self):
        new_message = messages.Message(title=messages.GET_WORLD,
                                       time=time.time(),
                                       content={},
                                       author=self.app.id,
                                       receiver="server")
        self.app.send_message(new_message)

    def create_world(self, name, type, private, owner):
        new_message = messages.Message(title=messages.CREATE_WORLD,
                                       time=time.time(),
                                       content={"type": type,
                                                "owner": owner,
                                                "private": private,
                                                "name":name},
                                       author=self.app.id,
                                       receiver="server")
        self.app.send_message(new_message)


class GamingState(State):
    pass

