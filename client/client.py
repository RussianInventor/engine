import sys
from common.exchange import Client
from .interface import create_interface, create_app


class ClientApp:
    def __init__(self, client_id, port):
        self.exchanger = Client(app=self, id=client_id, port=port)
        self.qt_app = create_app()
        self.interface = create_interface(self)

        self.world = None
        self.game = None

        self.state = None

    @property
    def user(self):
        return self.exchanger.user

    def run(self):
        self.interface.start()
        sys.exit(self.qt_app.exec_())

    def set_state(self, state_cls, **kwargs):
        self.state = state_cls(self, **kwargs)
