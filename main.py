from common.game import Game
from server.server import Server
import threading
server = Server("localhost", 4000)
game = Game(None, None)

server_thread = threading.Thread(target=server.listen)
game_thread = threading.Thread(target=game.update)
server.set_from_queue(game.events)
server_thread.start()
game_thread.start()
server_thread.join()
game_thread.join()
