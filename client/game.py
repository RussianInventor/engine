from queue import Queue
from client import config
from common.config import Config as GameConfig
from common.world import World


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self, app, players, world: World):
        self.app = app
        self.world = world
        self.players = players
        self.keyboard = config.Keyboard()

        self.update_queue = Queue()

    def process_updates(self):
        while not self.update_queue.empty():
            msg = self.update_queue.get()
            for obj in msg.content["objects"]:
                y = int(obj.pop("old_y") // GameConfig.CHUNK_SIZE)
                x = int(obj.pop("old_x") // GameConfig.CHUNK_SIZE)
                current_chunk = self.app.game.world.chunks[y][x]
                id = obj.pop("id")
                creature = current_chunk.objects[id]
                for atr, val in obj.items():
                    creature.__setattr__(atr, val)
                self.world.switch_chunk(current_chunk, creature)

    def update(self):
        self.process_updates()