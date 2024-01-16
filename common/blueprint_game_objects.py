from abc import ABC
import json
from common.config import Config


class ObjectBlueprint(ABC):
    def __init__(self, x, y, img_name):
        self.x = x
        self.y = y
        self.img_path = img_name

    @classmethod
    def from_json(cls, data):
        cls(**json.loads(data))

    def chunk_indexes(self):
        x = self.x//Config.CHUNK_SIZE
        y = self.y//Config.CHUNK_SIZE
        return x, y


class Item(ObjectBlueprint):
    def __init__(self, x, y, img_name):
        super().__init__(x=x, y=y, img_name=img_name)


class Creature(ObjectBlueprint):
    def __init__(self, x, y, img_name, hp, dx, dy, max_hp):
        super().__init__(x=x, y=y, img_name=img_name)
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
    def __init__(self, x, y, img_name, hp, max_hp):
        super().__init__(x=x, y=y, img_name=img_name)
        self._hp = hp
        self.max_hp = max_hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, val):
        self._hp = min(val, self.max_hp)
