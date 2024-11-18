import queue
import time
from .data_base import new_session
from common import model
from sqlalchemy import and_
from server import config as server_config
from common import a_non_i
from common.world import World
from common.blueprint_game_objects import Creature


class Game:
    EVENTS_UPDATE_LIMIT = 1000

    def __init__(self, app, world: World, game_id):
        self.app = app
        self.world = world
        self.players = {}
        self.events = queue.Queue()
        self.game_id = game_id

    def add_player(self, id):
        with new_session() as session:
            player = session.query(model.Player).filter(and_(model.Player.id == id,
                                                             model.Player.game_id == self.game_id)).first()
            if player is None:
                player = model.Player(id=id, game_id=self.game_id, obj_id=None)

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
            time.sleep(0.1/len(self.players))
            duration = time.time() - start_time
            if duration < server_config.Config.tick_duration:
                time.sleep(server_config.Config.tick_duration - duration)
