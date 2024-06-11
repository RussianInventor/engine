import math
import random
import select
import uuid
from abc import ABC
import json
from common.config import Config


DEFAULT = 'default'


class ObjectBlueprint(ABC):
    def __init__(self, x, y, id=None, **kwargs):
        self.images = {}
        self.id = str(uuid.uuid4()) if id is None else id
        self.w = 10
        self.h = 10
        self.x = x
        self.y = y
        self._img_name = None
        self.shift_img_x = 0.5
        self.shift_img_y = 1
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def img_key(self):
        return self.images.get(DEFAULT)

    def add_img_key(self, new_img, key: str = DEFAULT):
        if key not in self.images.keys():
            self.images[key] = new_img

    @property
    def img_name(self):
        if self._img_name is None:
            return f'{self.__class__.__name__}.png'
        return self._img_name

    @img_name.setter
    def img_name(self, img):
        self._img_name = img

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
    def __init__(self, x, y, hp, max_hp, v, **kwargs):
        super().__init__(x=x, y=y, **kwargs)
        self.v = v
        self.vx = 0
        self.vy = 0
        self._hp = hp
        self._max_hp = max_hp
        self.brain = None

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, val):
        self._hp = min(val, self._max_hp)

    def speed(self, x, y):
        dx = x - self.x
        dy = y - self.y
        d = math.sqrt(dx**2 + dy**2)
        cos = dx/d
        sin = dy/d
        self.vx = cos*self.v
        self.vy = sin*self.v

    def move(self, x, y):
        if x - self.x > self.vx and y - self.y > self.vy:
            self.x += self.vx
            self.y += self.vy
            return False
        else:
            self.x = x
            self.y = y
            return True


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
