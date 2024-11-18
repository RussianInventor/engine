import queue
import random
import time
from .data_base import new_session
from common import model
from sqlalchemy import and_
from server import config as server_config
from common import a_non_i
from common.world import World
from common.blueprint_game_objects import Creature
from common.game_objects import Human


class Game:
    EVENTS_UPDATE_LIMIT = 1000

    def __init__(self, app, world: World, game_id):
        self.app = app
        self.world = world
        self.players = {}
        self.events = queue.Queue()
        self.game_id = game_id
        self.new_objects = []

    def add_player(self, id):
        with new_session() as session:
            player = session.query(model.Player).filter(and_(model.Player.id == id,
                                                             model.Player.game_id == self.game_id)).first()
            if player is None:
                human = Human(random.randint(0, self.world.size[0]),
                              random.randint(0, self.world.size[1]))
                self.new_objects.append(human)
                self.world.add_object(human)
                player = model.Player(id=id, game_id=self.game_id, obj_id=human.id)
                session.add(player)
            self.players[id] = player

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
            new_objects = []
            for _ in range(len(self.new_objects)):
                new_objects.append(new_objects.pop(0))
            self.app.exchanger.broadcast(chunks=[], objects=updates, new_objects=new_objects)
            try:
                time.sleep(0.1 / len(self.players))
            except ZeroDivisionError:
                time.sleep(0.1)
            duration = time.time() - start_time
            if duration < server_config.Config.tick_duration:
                time.sleep(server_config.Config.tick_duration - duration)
