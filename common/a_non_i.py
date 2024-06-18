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
        self.state.update()


class State(ABC):
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def update(self):
        pass


class CalmState(State):
    def __init__(self, context):
        super().__init__(context=context)
        self.target = None

    def select_target(self):
        self.target = (random.randint(0, len(self.context.world.chunks)*Config.CHUNK_SIZE),
                       random.randint(0, len(self.context.world.chunks)*Config.CHUNK_SIZE))

    def update(self):
        if self.target is None:
            self.select_target()
        if self.context.obj.move(*self.target):
            self.select_target()
