import json
import time as t
from socket import socket


class MessageType:
    CONNECT = "connect"
    GET_WORLD = "get_world"
    RUN_GAME = "run_game"
    CREATE_WORLD = "create_world"
    WORLD_LIST = "world_list"


class Message:
    def __init__(self, connection: socket, title: str, time: float, content: dict, author: str, receiver: str):
        self.connection = connection
        self.title = title
        if time is None:
            self.time = t.time()
        else:
            self.time = time
        self.author = author
        self.receiver = receiver
        self.content = content

    @property
    def type(self):
        return self.title

    @classmethod
    def from_json(cls, connection, data):
        data = json.loads(data)
        return Message(connection=connection, **data.items())

    def json(self):
        data = {'title': self.title,
                'time': self.time,
                'author': self.author,
                'receiver': self.receiver,
                'content': self.content}
        return json.dumps(data)

    def answer(self, content: dict):
        msg = Message(connection=self.connection,
                      title=f're:{self.title}',
                      content=content,
                      time=t.time(),
                      author=self.receiver,
                      receiver=self.author)
        self.connection.send(msg.json().encode('utf-8'))
