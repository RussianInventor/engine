from .blueprint_game_objects import Creature


class InvisibleWashingMachine(Creature):
    def __init__(self):
        super().__init__(x=0, y=0, hp=1, max_hp=1, v=0, vision=0)
