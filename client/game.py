import queue
from client import config
from common import world


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self, app, players, world_id):
        self.app = app
        self.world = self.load_world(world_id)
        self.players = players
        self.events = queue.PriorityQueue()
        self.messages = queue.PriorityQueue()
        self.keyboard = config.Keyboard()

    def load_world(self, world_id):
        pass
        #world.
