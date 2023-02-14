import json
from common import model
from sqlalchemy import and_
from . import game_objects
from common.config import Config


class Storable:
    def create_json(self):
        json.dumps(self)
        return json

    def write(self):
        obj = vars(model)[self.__class__.__name__]()


class Chunk(Storable):
    w = Config.CHUNK_SIZE
    h = Config.CHUNK_SIZE

    def __init__(self):
        self.creatures = []
        self.items = []

    @classmethod
    def from_db(cls, chunk):
        return cls()

    def add_obj(self, obj):
        if isinstance(obj, game_objects.Item):
            self.items.append(obj)
        else:
            self.creatures.append(obj)


class World(Storable):
    def __init__(self, type):
        self.chunks = []
        self.time = 0
        self.max_day_time = 2400
        self.day = 0
        self.day_time = None
        self.type = type

    @classmethod
    def from_db(cls, session, world_id):
        world = session.query(model.World).filter(model.World.id == world_id).first()
        new_world = cls(world.type)
        y = 0
        while True:
            chunks = session.query(model.Chunk).filter(and_(model.Chunk.world_id == world_id,
                                                            model.Chunk.y == y)).order_by(model.Chunk.x.asc()).all()
            if not chunks:
                break
            new_world.chunks.append([])
            for chunk in chunks:
                new_world.chunks[-1].append(Chunk.from_db(chunk))
        objs = session.query(model.Object).filter(model.Object.world_id == world_id).all()
        clses = vars(game_objects)
        for obj in objs:
            cur_cls = clses[obj.cls]
            g_obj = cur_cls.from_json(obj.data)
            x, y = g_obj.chunk_indexes()
            new_world.chunks[y][x].add_obj(obj)
        return new_world

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
