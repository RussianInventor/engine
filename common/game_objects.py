from . import blueprint_game_objects


class Tree(blueprint_game_objects.Building):
    def __init__(self, x, y, img_name, hp, max_hp=None):
        if max_hp is None:
            max_hp = hp
        super().__init__(x=x, y=y, img_name=img_name, hp=hp, max_hp=max_hp)

