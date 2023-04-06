from common.game import Game
from common.app.app import Server
from server.config import Config
import threading
server = Server(Config.host, Config.port)
# game = Game(None, None)

server_thread = threading.Thread(target=server.listen)
client_thread = threading.Thread(target=server.listen_clients)
# game_thread = threading.Thread(target=game.update)

# server.set_from_queue(game.events)
print('run main thread')
server_thread.start()
print('run client thread')
client_thread.start()

# game_thread.start()
server_thread.join()
client_thread.join()
# game_thread.join()
