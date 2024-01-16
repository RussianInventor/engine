import json
from common import model
from sqlalchemy import and_, insert
from . import blueprint_game_objects, game_objects
from common.config import Config


class Storable:
    def create_json(self):
        json.dumps(self)
        return json

    def from_json(self, data):
        data = json.loads(data)

    def write(self):
        obj = vars(model)[self.__class__.__name__]()


class Chunk(Storable):
    w = Config.CHUNK_SIZE
    h = Config.CHUNK_SIZE

    def __init__(self, id, x, y, biome):
        self.creatures = []
        self.items = []
        self.buildings = []
        self.id = id
        self.x = x
        self.y = y
        self.biome = biome

    @classmethod
    def load(cls, chunk):
        return cls(id=chunk.id, x=chunk.x, y=chunk.y, biome=chunk.biome)

    def add_obj(self, obj):
        if isinstance(obj, blueprint_game_objects.Item):
            self.items.append(obj)
        elif isinstance(obj, blueprint_game_objects.Creature):
            self.creatures.append(obj)
        else:
            self.buildings.append(obj)


class World(Storable):
    def __init__(self, type, id):
        self.id = id
        self.chunks = []
        self.time = 0
        self.max_day_time = 2400
        self.day = 0
        self.day_time = None
        self.type = type

    @classmethod
    def load(cls, world_obj, chunks_objs, object_objs):
        new_world = cls(world_obj.type, id=world_obj.id)
        for chunk in chunks_objs:
            if len(new_world.chunks) == chunk.y:
                new_world.chunks.append([])
            new_world.chunks[-1].append(Chunk.load(chunk))

        clses = vars(game_objects)
        for obj in object_objs:
            cur_cls = clses[obj.cls]
            g_obj = cur_cls.from_json(obj.data)
            x, y = g_obj.chunk_indexes()
            new_world.chunks[y][x].add_obj(obj)
        return new_world

    def save(self, session):
        chunks = session.query(model.Chunk).filter(model.Chunk.world_id == self.id).all()
        for chunk in chunks:
            game_chunk = self.chunks[chunk.y][chunk.x]
            chunk.biome = game_chunk.biome
        # TODO такую же штуку для objects

    @classmethod
    def from_db(cls, session, world_id):
        world_obj = session.query(model.World).filter(model.World.id == world_id).first()
        chunk_objs = session.query(model.Chunk).filter(model.Chunk.world_id == world_id).order_by(model.Chunk.y.asc(),
                                                                                                  model.Chunk.x.asc()).all()
        object_objs = session.query(model.Object).filter(model.Object.world_id == world_id).all()

        return cls.load(world_obj=world_obj,
                        chunks_objs=chunk_objs,
                        object_objs=object_objs)

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
