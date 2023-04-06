import logging
from common.game import Game
from server.server import Server
from server.config import Config
import threading

logging.basicConfig(format="%(pathname)s \t %(message)s")
log = logging.getLogger()
log.addHandler(logging.FileHandler("log/server.log"))
log.setLevel(logging.DEBUG)

server = Server(Config.host, Config.port)
# game = Game(None, None)

server_thread = threading.Thread(target=server.listen)
# game_thread = threading.Thread(target=game.update)

# server.set_from_queue(game.events)

server_thread.start()
# game_thread.start()
server_thread.join()
# game_thread.join()
