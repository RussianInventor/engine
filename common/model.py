from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from enum import Enum
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP, INTEGER, FLOAT, BOOLEAN, JSON, ARRAY

Base = declarative_base()


class Item:
    def get_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Biome(Enum):
    FIELD = "field"
    MOUNTAINS = "mountains"
    BEACH = "beach"
    WATER = "water"
    DESERT = "desert"
    MEGA_MOUNTAINS = "MEGA_MOUNTAINS"


class WorldType(Base, Item):
    __tablename__ = 'world_types'
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class ChunkType(Base, Item):
    __tablename__ = "chunk_types"
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class World(Base, Item):
    __tablename__ = 'worlds'
    id = Column(TEXT, primary_key=True)
    type = Column(TEXT, ForeignKey(WorldType.type))
    name = Column(TEXT)
    size = Column(INTEGER)

    def __init__(self, id, type, name, size):
        super().__init__()
        for key, val in locals().items():
            self.__setattr__(key, val)


class Chunk(Base, Item):
    __tablename__ = "chunks"
    id = Column(TEXT, primary_key=True)
    world_id = Column(TEXT, ForeignKey(World.id))
    x = Column(INTEGER)
    y = Column(INTEGER)
    biome = Column(TEXT, ForeignKey(ChunkType.type))

    def __init__(self, id, world_id, x, y, biome: Biome | str):
        super().__init__()
        for key, val in locals().items():
            self.__setattr__(key, val)
        if isinstance(biome, Biome):
            biome = biome.value
        self.biome = biome


class Object(Base, Item):
    __tablename__ = "objects"
    id = Column(TEXT, primary_key=True)
    world_id = Column(TEXT, ForeignKey(World.id))
    data = Column(JSON)
    cls = Column(TEXT)

    def __init__(self, id, world_id, data, cls):
        super().__init__()
        for key, val in locals().items():
            self.__setattr__(key, val)


class ObjectGen(Base, Item):
    __tablename__ = "object_gens"
    cls = Column(TEXT, primary_key=True)
    biome = Column(TEXT, ForeignKey(ChunkType.type))
    min_num_in_chunk = Column(INTEGER)
    max_num_in_chunk = Column(INTEGER)
    percent_chunks = Column(INTEGER)
    init_data = Column(TEXT)

    def __init__(self, cls, biome):
        super().__init__()
        for key, val in locals().items():
            self.__setattr__(key, val)


class GameInfo(Base, Item):
    __tablename__ = "game_info"
    game_id = Column(TEXT, primary_key=True)
    game_name = Column(TEXT)
    world_ids = Column(ARRAY(TEXT))
    players = Column(JSON)
    private = Column(BOOLEAN)
    owner = Column(TEXT)

    current_world_index = 0

    def __init__(self, game_id, game_name, world_ids, players, private, owner):
        super().__init__()
        for key, val in locals().items():
            self.__setattr__(key, val)
