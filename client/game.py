from queue import Queue
from client import config
from common.config import Config as GameConfig
from common.world import World
from .player import Player
from common import model


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self,
                 app,
                 world: World,
                 player_obj_id,
                 player_obj_data):
        self.app = app
        self.world = world
        self.keyboard = config.Keyboard()

        self.world.load_objs(object_objs=[model.Object(**player_obj_data)],
                             world=self.world)

        self.player = Player(obj=self.world.get_object(obj_id=player_obj_id),
                             world=self.world,
                             app=self.app)

        self.update_queue = Queue()

    def process_updates(self):
        while not self.update_queue.empty():
            msg = self.update_queue.get()
            for obj in msg.content.objects:
                y = int(obj.pop("old_y") // GameConfig.CHUNK_SIZE)
                x = int(obj.pop("old_x") // GameConfig.CHUNK_SIZE)
                obj_id = obj.pop("id")
                creature = self.world.get_object(obj_id)
                for atr, val in obj.items():
                    creature.__setattr__(atr, val)
                self.world.switch_chunk(creature)
            self.world.load_objs(object_objs=msg.content.new_objects,
                                 world=self.world)

    def update(self):
        while True:
            self.process_updates()
