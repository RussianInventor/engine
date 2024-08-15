import queue
import time
import warnings
from common import game_utils
from common import world
from client import config as client_config
from server import config as server_config
from common import a_non_i
from .exchange import exchanger

warnings.warn('старье', DeprecationWarning)


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


