import json
import time
from socket import socket

CONNECT = "connect"
GET_WORLD = "get_world"
RUN_GAME = "run_game"
CREATE_WORLD = "create_world"
WORLD_LIST = "world_list"


class Message:
    def __init__(self, connection: socket, title: str, time: float, content: dict, author: str, receiver: str):
        self.connection = connection
        self.title = title
        self.time = time
        self.author = author
        self.receiver = receiver
        self.content = content

    @classmethod
    def from_json(cls, connection, data):
        data = json.loads(data)
        return Message(connection=connection, **data.items())

    def json(self):
        data = {'title': self.title,
                'author': self.author,
                'receiver': self.receiver,
                'content': self.content}
        print(data)
        return json.dumps(data)

    def answer(self, content: dict):
        msg = Message(connection=self.connection,
                      title=f're:{self.title}',
                      content=content,
                      time=time.time(),
                      author=self.receiver,
                      receiver=self.author)
        self.connection.send(msg.json().encode('utf-8'))
