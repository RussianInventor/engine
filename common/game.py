import queue
import pygame
import game_utils
import world


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
        super(Object).__init__(x, y, w=10, h =10)
        super(Moving).__init__(v=1)


class Game:
    EVENTS_UPDATE_LIMIT = 100

    def __init__(self, players, world:world.World):
        self.world = world
        self.players = players
        self.events = queue.PriorityQueue()
        self.message = queue.PriorityQueue()

    def update(self):
        while True:
            for _ in range(0, self.EVENTS_UPDATE_LIMIT):
                if self.events.empty():
                    break
                _, event = self.events.get()
                print(event.time, event.author, event.other)
            for chunk in self.world.chunks:
                for creature in chunk.creatures:
                    print(creature.x, creature.y)

