import threading

from common.exchange import Server
from common.app import App

from .server_states import State


class ServerApp(App):
    def __init__(self, client_id, port):
        super().__init__()
        self.exchanger = Server(app=self, id=client_id, port=port)
        self.clients = {}
        self.game = None

        self.server_thread = threading.Thread(target=self.exchanger.listen)
        self.client_thread = threading.Thread(target=self.exchanger.listen_clients)
        self.game_thread = None

    def run_game(self):
        self.game_thread = threading.Thread(target=self.game.update)
        self.game_thread.start()

    def run(self):
        self.server_thread.start()
        self.client_thread.start()

        self.server_thread.join()
        self.client_thread.join()
