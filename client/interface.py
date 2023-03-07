import subprocess
from app.app import Client
from client.config import Config
from .client_state import IdleState
subprocess.call(("pyuic5",
                 "client/untitled.ui",
                 "-o",
                 "client/design.py"))
import sys
from PyQt5 import QtWidgets
from . import design


class InterApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, client: Client):
        super().__init__()
        self.setupUi(self)
        self.connectButton.clicked.connect(self.connect)
        self.client = client

    def connect(self):
        host = self.hostEntry.text()
        port = int(self.portEntry.text())
        if self.client.connect(host, port, Config.id, Config.port):
            self.show_idle_frame()
            self.client.set_state(IdleState)
        else:
            QtWidgets.QMessageBox(self, text="Проверьте адрес сервера и порт").show()

    def show_connection_frame(self):
        self.idle_frame.hide()
        self.
        self.connection_frame.show()

    def show_idle_frame(self):
        self.connection_frame.hide()
        for world in self.client.state.execute("get_world"):
            self.world_selection.addItem(text=world.name, userData=world.id)
        self.idle_frame.show()


def run_interface(client):
    app = QtWidgets.QApplication(sys.argv)
    window = InterApp(client)
    window.show()
    window.show_connection_frame()
    app.exec_()
