import threading

from common.exchange import Server
from .server_states import State


class ServerApp:
    def __init__(self, client_id, port):
        self.exchanger = Server(app=self, id=client_id, port=port)
        self.clients = {}
        self.game = None
        self.state = None

        self.server_thread = threading.Thread(target=self.exchanger.listen)
        self.client_thread = threading.Thread(target=self.exchanger.listen_clients)
        self.game_thread = None

    def set_state(self, state_cls: State.__class__, **kwargs):
        self.state = state_cls(self, **kwargs)

    def run(self):
        self.server_thread.start()
        self.client_thread.start()

        self.server_thread.join()
        self.client_thread.join()