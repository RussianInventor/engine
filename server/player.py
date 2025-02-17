import math
from common import blueprint_game_objects, game_objects


class Player:
    def __init__(self, obj: blueprint_game_objects.Creature, world):
        self.world = world
        self.obj = obj

    def update(self):
        before = self.obj.__dict__.copy()

        self.move()

        after = self.obj.__dict__
        update_dict = {}
        for atr, val in before.items():
            if val != after[atr]:
                update_dict[atr] = after[atr]
        if update_dict:
            update_dict.update({"id": self.obj.id, "old_x": self.obj.x, "old_y": self.obj.y})
            return update_dict

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
        return self.obj.v

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

    def create_stick(self):
        self.world.create_objects(objs=[game_objects.Stick(self.obj.x + 3, self.obj.y + 3)], sync=False)

    def take_item(self, item_id, index=None):
        item = self.world.get_object(item_id)
        return self.obj.inventory.add(item, index)
