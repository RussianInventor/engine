import json
from common import model


class Storable:
    def create_json(self):
        json.dumps(self)
        return json

    def write(self):
        obj = vars(model)[self.__class__.__name__]()


class Chunk(Storable):
    w = 100
    h = 100

    def __init__(self):
        self.creatures = []
        self.items = []


class World(Storable):
    def __init__(self):
        self.chunks = []
        self.time = 0
        self.max_day_time = 2400
        self.day = 0
        self.day_time = None

    def time_steps(self):
        self.time += 1
        if self.time / self.max_day_time == self.time // self.max_day_time:
            self.time = 0
            self.day += 1

        if 0 <= self.time < 400:
            self.day_time = "night"
        elif 400 <= self.time < 1200:
            self.day_time = "morning"
        elif 1200 <= self.time < 1800:
            self.day_time = "day"
        elif 1800 <= self.time < 2400:
            self.day_time = "evening"
