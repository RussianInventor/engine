import random
import uuid
from abc import ABC
import json
from common.config import Config


class ObjectBlueprint(ABC):
    def __init__(self, x, y, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.x = x
        self.y = y

    @classmethod
    def from_json(cls, data):
        cls(**json.loads(data))

    def to_json(self):
        ret = json.dumps(self.__dict__, ensure_ascii=False)
        return ret.replace("\\", "")

    def chunk_indexes(self):
        x = self.x // Config.CHUNK_SIZE
        y = self.y // Config.CHUNK_SIZE
        return x, y

    @classmethod
    def generation(cls, chunk, kwargs):
        return cls(x=random.randint(chunk.x * Config.CHUNK_SIZE, (1 + chunk.x) * Config.CHUNK_SIZE),
                   y=random.randint(chunk.y * Config.CHUNK_SIZE, (1 + chunk.y) * Config.CHUNK_SIZE),
                   **kwargs)


class Item(ObjectBlueprint):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)


class Creature(ObjectBlueprint):
    def __init__(self, x, y, hp, dx, dy, max_hp):
        super().__init__(x=x, y=y)
        self.dx = dx
        self.dy = dy
        self._hp = hp
        self._max_hp = max_hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, val):
        self._hp = min(val, self._max_hp)


class Building(ObjectBlueprint):
    def __init__(self, x, y, hp, max_hp):
        super().__init__(x=x, y=y)
        self._hp = hp
        self.max_hp = max_hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, val):
        self._hp = min(val, self.max_hp)
