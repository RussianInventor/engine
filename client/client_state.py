import time
import threading
from abc import ABC
from collections import namedtuple

from common.exchange.messages import DeleteGameRequest, CreateGameRequest, GameInfo
from common.model import Object

import common.world
from common.exchange import messages
from client import graphic
from client.game import Game

from common.config import Config as ComConfig
from queue import Queue


class State(ABC):
    def __init__(self, app):
        self.app = app

    def handle_message(self, msg):
        pass

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
        new_message = messages.Message(type=messages.MessageType.GET_WORLD,
                                       author=self.exchanger.user.user_id,
                                       receiver="server")
        answer = self.exchanger.send_message(new_message)
        return answer.content.worlds

    def delete_world(self, id, owner):
        new_message = messages.Message(type=messages.MessageType.DELETE_GAME,
                                       content=DeleteGameRequest(game_id=id),
                                       author=owner,
                                       receiver="server")
        answer = self.exchanger.send_message(new_message)

    def create_world(self, name, private, owner, size):
        new_message = messages.Message(type=messages.MessageType.CREATE_GAME,
                                       author=owner,
                                       receiver="server",
                                       content=CreateGameRequest(
                                           game=GameInfo(
                                               owner=owner,
                                               id=None,
                                               private=private,
                                               name=name,
                                               size=size)))
        answer = self.exchanger.send_message(new_message)


class GamingState(State):
    def __init__(self, app, world_id):
        super().__init__(app)
        new_message = messages.Message(connection=self.exchanger.connection,
                                       title=messages.MessageType.RUN_GAME,
                                       time=time.time(),
                                       content={"world_id": world_id},
                                       author=self.app.user.user_id,
                                       receiver="server.py")
        answer = self.exchanger.send_message(new_message)
        World = namedtuple('World', answer.content['world'])
        Chunk = namedtuple('Chunk', answer.content['chunks'][0])

        world = common.world.World.load(world_obj=World(**answer.content['world']),
                                        chunks_objs=[Chunk(**c) for c in answer.content['chunks']],
                                        object_objs=[Object(**o) for o in answer.content['objects']])
        self.app.game = Game(app=self.app,
                             players=[],
                             world=world)

        self.draw_world = graphic.DrawWorld(self.app)
        self.graphic_thread = threading.Thread(target=self.draw_world.update)
        self.graphic_thread.start()
        new_message = messages.Message(connection=self.exchanger.connection,
                                       title=messages.MessageType.CLIENT_READY,
                                       time=time.time(),
                                       content={},
                                       author=self.app.user.user_id,
                                       receiver="server")
        self.exchanger.send_message(new_message, answer_wait=False)

        self.app.run_game()

    def handle_message(self, msg):
        if msg.type == messages.MessageType.WORLD_UPDATE:
            self.app.game.update_queue.put(msg)
