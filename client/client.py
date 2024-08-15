import sys
from common.exchange import Client
from common.app import App
from client.interface.interface import create_interface, create_app


class ClientApp(App):
    def __init__(self, client_id, port):
        super().__init__()
        self.exchanger = Client(app=self, id=client_id, port=port)
        self.qt_app = create_app()
        self.interface = create_interface(self)

        self.game = None

    @property
    def user(self):
        return self.exchanger.user

    def run(self):
        self.interface.start()
        sys.exit(self.qt_app.exec_())
