import json


class Event:
    def __init__(self, time, author, other: dict):
        self.time = time
        self.author = author
        self.other = other

    def json(self):
        return json.dumps({"time": self.time, "author": self.author, "other": self.other})
