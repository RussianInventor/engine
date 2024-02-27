from . import blueprint_game_objects


class Tree(blueprint_game_objects.Building):
    def __init__(self, x, y, _hp, max_hp=None, **kwargs):
        if max_hp is None:
            max_hp = _hp
        super().__init__(x=x, y=y, hp=_hp, max_hp=max_hp, **kwargs)
