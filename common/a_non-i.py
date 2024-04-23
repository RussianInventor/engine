from abc import ABC, abstractmethod
import random
from .config import Config


class Context:
    def __init__(self, obj, state, world):
        self.world = world
        self.obj = obj
        self.state = state

    def switch_to(self, new_state):
        self.state = new_state(self)


class State(ABC):
    def __init__(self, context):
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
        pass
