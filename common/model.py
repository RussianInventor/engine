from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from enum import Enum
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP, INTEGER, FLOAT, BOOLEAN, JSON
Base = declarative_base()


class Biome(Enum):
    FIELD = "field"
    MOUNTAINS = "mountains"
    BEACH = "beach"
    WATER = "water"
    MEGA_MOUNTAINS = "MEGA_MOUNTAINS"

class WorldType(Base):
    __tablename__ = 'world_types'
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class ChunkType(Base):
    __tablename__ = "chunk_types"
    type = Column(TEXT, primary_key=True)
    description = Column(TEXT)


class World(Base):
    __tablename__ = 'worlds'
    id = Column(TEXT, primary_key=True)
    type = Column(TEXT, ForeignKey(WorldType.type))
    owner = Column(TEXT)
    private = Column(BOOLEAN)
    name = Column(TEXT)
    size = Column(INTEGER)

    def __init__(self, id):
        for key, val in locals().items():
            self.__setattr__(key, val)


class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(TEXT, primary_key=True)
    world_id = Column(TEXT, ForeignKey(World.id))
    x = Column(INTEGER)
    y = Column(INTEGER)
    biome = Column(TEXT, ForeignKey(ChunkType.type))

    def __init__(self, id, world_id, x, y, biome: Biome):
        for key, val in locals().items():
            self.__setattr__(key, val)
        self.biome = biome.value


class Object(Base):
    __tablename__ = "objects"
    id = Column(TEXT, primary_key=True)
    world_id = Column(TEXT, ForeignKey(World.id))
    data = Column(JSON)
    cls = Column(TEXT)
