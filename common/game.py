import queue
import time
from common import game_utils
from common import world
from client import config as client_config
from server import config as server_config
from common import a_non_i
from .exchange import exchanger


class Player:
    def __init__(self, id, connection):
        self.id = id
        self.connection = connection

    def send_command(self, command):
        pass


class Object:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Moving:
    def __init__(self, v):
        self.v = v
        self.vx = 0
        self.vy = 0

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        d = game_utils.dist(self.x, self.y, target_x, target_y)
        cos = dx / d
        sin = dy / d
        self.vx = cos * self.v
        self.vy = sin * self.v
        self.x += self.vx
        self.y += self.vy


class I(Object, Moving):
    def __init__(self, x, y):
        super(Object).__init__(x, y, w=10, h=10)
        super(Moving).__init__(v=1)


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self, app, players, world_id):
        self.app = app
        self.world_id = world_id
        self.world = None
        self.players = players
        self.events = queue.PriorityQueue()
        self.messages = queue.PriorityQueue()
        self.keyboard = client_config.Keyboard()

    def load_a_non_i(self):
        for row in self.world.chunks:
            for chunk in row:
                for creature in chunk.creatures:
                    creature.brain = a_non_i.Context(obj=creature, state=a_non_i.CalmState, world=self.world)

    def update(self):
        while True:
            start_time = time.time()
            for _ in range(0, self.EVENTS_UPDATE_LIMIT):
                if self.events.empty():
                    break
                _, event = self.events.get()
                print(event.time, event.author, event.other)
            update_object_list = []
            for row in self.world.chunks:
                for chunk in row:
                    for creature in chunk.creatures:
                        update_object_list.append(creature.brain.update())
            self.app.exchanger.send_update(chunks=[], objects=update_object_list)
            duration = time.time() - start_time
            if duration < server_config.Config.tick_duration:
                time.sleep(server_config.Config.tick_duration - duration)
