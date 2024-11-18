import math
from common import blueprint_game_objects


class Player:
    def __init__(self, obj: blueprint_game_objects.Creature, world):
        self.world = world
        self.obj = obj

    @property
    def x(self):
        return self.obj.x

    @property
    def y(self):
        return self.obj.y

    @property
    def v_x(self):
        return self.obj.v_x

    @property
    def v_y(self):
        return self.obj.v_y

    @v_x.setter
    def v_x(self, val):
        self.obj.v_x = val

    @v_y.setter
    def v_y(self, val):
        self.obj.v_y = val

    @property
    def step(self):
        return 1

    def down(self):
        self.v_y = self.step

    def up(self):
        self.v_y = -self.step

    def right(self):
        self.v_x = self.step

    def left(self):
        self.v_x = -self.step

    def stop_x(self):
        self.v_x = 0

    def stop_y(self):
        self.v_y = 0

    def move(self):
        if self.v_y != 0 and self.v_x != 0:
            self.obj.x += self.obj.v / math.sqrt(2) * self.v_x
            self.obj.y += self.obj.v / math.sqrt(2) * self.v_y
        else:
            self.obj.x += self.obj.v * self.v_x
            self.obj.y += self.obj.v * self.v_y
