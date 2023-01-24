from abc import ABC
import json
from common.config import Config


class ObjectBlueprint(ABC):
    @classmethod
    def from_json(cls, data):
        cls(**json.loads(data))

    def chunk_indexes(self):
        x = self.x//Config.CHUNK_SIZE
        y = self.y//Config.CHUNK_SIZE
        return x, y


class Item(ObjectBlueprint):
    pass


class Creature(ObjectBlueprint):
    pass
