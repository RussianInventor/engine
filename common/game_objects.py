from . import blueprint_game_objects
import random
import os
from .config import Config


class Tree(blueprint_game_objects.Building):
    def __init__(self, x, y, _hp, max_hp=None, **kwargs):
        if max_hp is None:
            max_hp = _hp
        super().__init__(x=x, y=y, hp=_hp, max_hp=max_hp, **kwargs)
        self.img_name = random.choice(os.listdir(os.path.join(Config.SOURCE, "img", "tree")))


class Pig(blueprint_game_objects.Creature):
    def __init__(self, x, y, _hp, max_hp=None, **kwargs):
        if max_hp is None:
            max_hp = _hp
        super().__init__(x=x, y=y, hp=_hp, max_hp=max_hp, **kwargs)
