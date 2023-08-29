import logging
import argparse
from common.game import Game
from server.server import ServerApp
from server.config import Config
import threading
from server.server_states import IdleState

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=False, default=Config.port)
port = parser.parse_args().port
f = open("log/server.py.log", mode="w")
f.close()
logging.basicConfig(format="%(pathname)s \t %(message)s", filemode="w")
log = logging.getLogger()
log.addHandler(logging.FileHandler("log/server.py.log"))
log.setLevel(logging.DEBUG)

server = ServerApp(Config.host, port)
server.set_state(IdleState)
server.run()
