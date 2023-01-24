import json

CONNECT = "connect"
GET_WORLD = "get_world"
RUN_GAME = "run_game"
CREATE_WORLD = "create_world"
WORLD_LIST = "world_list"


class Message:
    def __init__(self, title: str, time: float, content: dict, author: str, receiver: str):
        self.title = title
        self.time = time
        self.author = author
        self.receiver = receiver
        self.content = content

    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        return Message(**data.items())

    def json(self):
        data = {'title': self.title,
                'author': self.author,
                'receiver': self.receiver,
                'content': self.content}
        return json.dumps(data)
