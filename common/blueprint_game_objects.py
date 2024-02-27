import random
import uuid
from abc import ABC
import json
from common.config import Config


class ObjectBlueprint(ABC):
    def __init__(self, x, y, id=None, **kwargs):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.x = x
        self.y = y
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def img_name(self):
        return f'{self.__class__.__name__}.png'

    @classmethod
    def from_json(cls, data):
        return cls(**json.loads(data))

    def to_json(self):
        ret = json.dumps(self.__dict__)
        return ret

    def chunk_indexes(self):
        x = self.x // Config.CHUNK_SIZE
        y = self.y // Config.CHUNK_SIZE
        return x, y

    @classmethod
    def generation(cls, chunk, kwargs):
        return cls(x=random.randint(chunk.x * Config.CHUNK_SIZE, (1 + chunk.x) * Config.CHUNK_SIZE-1),
                   y=random.randint(chunk.y * Config.CHUNK_SIZE, (1 + chunk.y) * Config.CHUNK_SIZE-1),
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
    def __init__(self, x, y, hp, max_hp, **kwargs):
        super().__init__(x=x, y=y, **kwargs)
        self._hp = hp
        self.max_hp = max_hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, val):
        self._hp = min(val, self.max_hp)
