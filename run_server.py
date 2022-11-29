from common.game import Game
from server.server import Server
from server.config import Config
import threading
server = Server(Config.host, Config.port)
# game = Game(None, None)

server_thread = threading.Thread(target=server.listen)
# game_thread = threading.Thread(target=game.update)

# server.set_from_queue(game.events)
print('run main thread')
server_thread.start()
# game_thread.start()
server_thread.join()
# game_thread.join()
