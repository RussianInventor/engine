import queue
import time
import pygame
from common import game_utils
from common import world
from client import config
from server.config import Config
from common.data_base import new_session


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


# class Pygame:
#     def __init__.py(self, game):
#         self.screen = None
#         self.game = game
#
#     def start(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((500, 500))
#         while True:
#             self.update()
#
#     def check_key(self, key_code):
#         command = self.game.keyboard.get_key(key_code)
#         if command is not None:
#             command()
#
#     def update(self):
#         start_time = time.time()
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 self.check_key(event.key)
#             if event.type == pygame.QUIT:
#                 exit()
#         pygame.display.update()
#
#         duration = time.time() - start_time
#         if duration < config.Config.frame_duration:
#             time.sleep(config.Config.frame_duration - duration)


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self, app, players, world_id):
        self.app = app
        self.world = self.load_world(world_id)
        self.players = players
        self.events = queue.PriorityQueue()
        self.messages = queue.PriorityQueue()
        self.keyboard = config.Keyboard()

    @staticmethod
    def load_world(world_id):
        with new_session() as session:
            return world.World.from_db(session, world_id)

    def update_pygame(self):
        pass

    def update(self):
        start_time = time.time()
        while True:
            for _ in range(0, self.EVENTS_UPDATE_LIMIT):
                if self.events.empty():
                    break
                _, event = self.events.get()
                print(event.time, event.author, event.other)
            for chunk in self.world.chunks:
                for creature in chunk.creatures:
                    print(creature.x, creature.y)
            duration = time.time() - start_time
            if duration < Config.tick_duration:
                time.sleep(Config.tick_duration - duration)
