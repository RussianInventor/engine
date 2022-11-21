import socket
import json
import threading
import time
import uuid
from client.config import Config
from common.connection_utils import read_message
from client.client import Client
from common.game import Game, Pygame

client = Client(host=Config.server_host,
                port=Config.server_port,
                listening_port=Config.port)

game = Game(None, None)
interface = Pygame(game)
client.set_to_queue(game.messages)
client.set_from_queue(game.events)
client_thread = threading.Thread(target=client.connect)
game_thread = threading.Thread(target=game.update)
interface_thread = threading.Thread(target=interface.start)
client_thread.start()
game_thread.start()
interface_thread.start()
