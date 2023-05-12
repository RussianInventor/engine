import subprocess
from common.app.app import Client
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
        self.client = client
        self.connectButton.clicked.connect(self.connect)
        self.new_world.clicked.connect(lambda: self.show_frame('world_frame'))
        self.create_button.clicked.connect(lambda: self.client.state.execute("create_world",
                                                                             {"name": self.world_name.text(),
                                                                              "type": "ground",
                                                                              "private": self.world_private.isChecked(),
                                                                              "owner": Config.id}))

    def connect(self):
        host = self.hostEntry.text()
        port = int(self.portEntry.text())
        if self.client.connect(host, port, Config.id, Config.port):
            self.show_frame('idle_frame', on_load=self.load_worlds)
            self.client.set_state(IdleState)
        else:
            QtWidgets.QMessageBox(self, text="Проверьте адрес сервера и порт").show()

    def show_frame(self, frame_name, on_load=None):
        if on_load is not None:
            on_load()
        for frame in filter(lambda w: isinstance(w, QtWidgets.QFrame), self.centralwidget.children()):
            if frame.objectName() == frame_name:
                frame.show()
            else:
                frame.hide()

    def load_worlds(self):
        for world in self.client.state.execute("get_world"):
            self.world_selection.addItem(text=world.name, userData=world.id)


def run_interface(client):
    app = QtWidgets.QApplication(sys.argv)
    window = InterApp(client)
    window.show()
    window.show_frame('connection_frame')
    app.exec_()
