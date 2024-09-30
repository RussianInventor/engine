import logging
import argparse
from common.game import Player
from server.server import ServerApp
from server.config import Config
import threading
from server.server_states import IdleState
import sys


class Logger(logging.Logger):
    def __init__(self):
        self.lines = 0
        self.max_lines = 5000

    def info(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        self.lines += 1
        if self.lines > self.max_lines:
            f = open("log/server.log", mode="w")
            f.close()
        super().info(**locals())


# logging.setLoggerClass(Logger)
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=False, default=Config.port)
port = parser.parse_args().port
f = open("log/server.log", mode="w")
f.close()
logging.basicConfig(format="%(levelname)s \t %(pathname)s \t %(message)s", filemode="w")
log = logging.getLogger()
log.addHandler(logging.FileHandler("log/server.log"))
log.setLevel(logging.DEBUG)
sys.stderr = open("log/server.err", mode="w")
server = ServerApp(Config.host, port)
server.set_state(IdleState)
server.run()