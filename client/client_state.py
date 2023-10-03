import time
import threading
from abc import ABC
from collections import namedtuple
from common.model import Object

import common.world
from common.exchange import messages
from client import graphic
from common.config import Config as ComConfig


class State(ABC):
    def __init__(self, app):
        self.app = app

    @property
    def exchanger(self):
        return self.app.exchanger

    def execute(self, function_name, kwargs=None):
        if kwargs is None:
            kwargs = {}
        return getattr(self, function_name)(**kwargs)


class InitState(State):
    def connect(self, host, port, name, listening_port):
        self.exchanger.connect(host=host, port=port, name=name, listening_port=listening_port)


class IdleState(State):
    # def run_game(self, world_id):
    #     new_message = messages.Message(connection=self.exchanger.connection,
    #                                    title=messages.MessageType.RUN_GAME,
    #                                    time=time.time(),
    #                                    content={"world_id": world_id},
    #                                    author=self.exchanger.user.user_id,
    #                                    receiver="server.py")
    #     self.exchanger.send_message(new_message)

    def get_world(self):
        new_message = messages.Message(connection=self.exchanger.connection,
                                       title=messages.MessageType.GET_WORLD,
                                       time=time.time(),
                                       content={},
                                       author=self.exchanger.user.user_id,
                                       receiver="server.py")
        answer = self.exchanger.send_message(new_message)
        if answer.has_error():
            return []
        return answer.content.get('worlds')

    def delete_world(self, id, owner):
        new_message = messages.Message(connection=self.exchanger.connection,
                                       title=messages.MessageType.DELETE_WORLD,
                                       time=time.time(),
                                       content={"id": id},
                                       author=owner,
                                       receiver="server.py")
        answer = self.exchanger.send_message(new_message)

    def create_world(self, name, type, private, owner, size):
        new_message = messages.Message(connection=self.exchanger.connection,
                                       title=messages.MessageType.CREATE_WORLD,
                                       time=time.time(),
                                       content={"type": type,
                                                "owner": owner,
                                                "private": private,
                                                "name": name,
                                                "size": size},
                                       author=owner,
                                       receiver="server.py")
        print(new_message.content)
        answer = self.exchanger.send_message(new_message)
        print('>>>', answer)


class GamingState(State):
    def __init__(self, app):
        super().__init__(app)
        self.draw_world = graphic.DrawWorld(self.app)
        new_message = messages.Message(connection=self.exchanger.connection,
                                       title=messages.MessageType.RUN_GAME,
                                       time=time.time(),
                                       content={"world_id": self.app.game.world_id},
                                       author=self.app.user.user_id,
                                       receiver="server.py")
        answer = self.exchanger.send_message(new_message)
        new_message = messages.Message(connection=self.exchanger.connection,
                                       title=messages.MessageType.GET_WORLD_FULL_INFO,
                                       time=time.time(),
                                       content={"world_id": self.app.game.world_id},
                                       author=self.app.user.user_id,
                                       receiver="server.py")
        answer = self.exchanger.send_message(new_message)
        World = namedtuple('World', answer.content['world'])
        Chunk = namedtuple('Chunk', answer.content['chunks'][0])

        self.app.game.world = common.world.World.load(world_obj=World(**answer.content['world']),
                                                      chunks_objs=[Chunk(**c) for c in answer.content['chunks']],
                                                      object_objs=[Object(**o) for o in answer.content['objects']])

    def run_thread(self):
        thread = threading.Thread(target=self.draw_world.update)
        return thread
