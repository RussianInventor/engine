import queue
import time
from server import config as server_config
from common import a_non_i
from common.world import World
from common.blueprint_game_objects import Creature


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self, app, players, world: World):
        self.app = app
        self.world = world
        self.players = players
        self.events = queue.Queue()

    def load_a_non_i(self):
        for obj in self.world.objects(base_cls=Creature):
            obj.brain = a_non_i.Context(obj=obj,
                                        state=a_non_i.CalmState,
                                        world=self.world)

    def update(self):
        while True:
            start_time = time.time()
            updates = []
            for creature in self.world.objects(base_cls=Creature):
                updates.append(creature.brain.update())
            self.app.exchanger.broadcast(chunks=[], objects=updates)
            time.sleep(0.1)
            duration = time.time() - start_time
            if duration < server_config.Config.tick_duration:
                time.sleep(server_config.Config.tick_duration - duration)
