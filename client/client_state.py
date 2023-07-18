import time
from abc import ABC
from common.app import messages
from common.app.app import Client

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
        new_message = messages.Message(connection=self.app.connection,
                                       title=messages.MessageType.RUN_GAME,
                                       time=time.time(),
                                       content={"world_id": world_id},
                                       author=self.app.user.user_id,
                                       receiver="server")
        self.app.send_message(new_message)

    def get_world(self):
        new_message = messages.Message(connection=self.app.connection,
                                       title=messages.MessageType.GET_WORLD,
                                       time=time.time(),
                                       content={},
                                       author=self.app.user.user_id,
                                       receiver="server")
        answer = self.app.send_message(new_message)
        if answer.has_error():
            return []
        return answer.content.get('worlds')

    def delete_world(self, id, owner):
        new_message = messages.Message(connection=self.app.connection,
                                       title=messages.MessageType.DELETE_WORLD,
                                       time=time.time(),
                                       content={"id": id},
                                       author=owner,
                                       receiver="server")
        print(new_message.content)
        answer = self.app.send_message(new_message)
        print('>>>', answer)

    def create_world(self, name, type, private, owner, size):
        new_message = messages.Message(connection=self.app.connection,
                                       title=messages.MessageType.CREATE_WORLD,
                                       time=time.time(),
                                       content={"type": type,
                                                "owner": owner,
                                                "private": private,
                                                "name": name,
                                                "size": size},
                                       author=owner,
                                       receiver="server")
        print(new_message.content)
        answer = self.app.send_message(new_message)
        print('>>>', answer)


class GamingState(State):
    pass
