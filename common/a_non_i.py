from abc import ABC, abstractmethod
import random
from .config import Config
from common import blueprint_game_objects


class Context:
    def __init__(self, obj: blueprint_game_objects.Creature, state, world):
        self.world = world
        self.obj = obj
        self.state = None
        self.switch_to(state)

    def switch_to(self, new_state):
        self.state = new_state(self)

    def update(self):
        before = self.obj.__dict__.copy()
        self.state.update()
        after = self.obj.__dict__
        update_list = {}
        for atr, val in before.items():
            if val != after[atr]:
                update_list[atr] = after[atr]
        if update_list:
            update_list.update({"id": self.obj.id, "old_x": self.obj.x, "old_y": self.obj.y})
            return update_list


class State(ABC):
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def update(self):
        pass

    def __repr__(self):
        return self.__class__.__name__


class CalmState(State):
    def __init__(self, context):
        super().__init__(context=context)
        self.target = None

    def select_target(self):
        self.target = (random.randint(0, len(self.context.world.chunks)*Config.CHUNK_SIZE),
                       random.randint(0, len(self.context.world.chunks)*Config.CHUNK_SIZE))
        self.context.obj.speed(*self.target)

    def update(self):
        if self.target is None:
            self.select_target()
        if self.context.obj.move(*self.target):
            self.target = None

    def __repr__(self):
        return f'{self.__class__.__name__} (target={self.target})'
