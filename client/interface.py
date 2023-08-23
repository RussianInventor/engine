import logging
import subprocess
from common.app.app import Client
from common.config import Config as ComConfig
from client.config import Config
from .client_state import IdleState
from .graphic import draw_chunks
from PyQt5.QtWidgets import QGraphicsScene
from common import model
from common.data_base import new_session
from common.game import Game


subprocess.call(("pyuic5",
                 "client/untitled.ui",
                 "-o",
                 "client/design.py"))
import sys
from PyQt5 import QtWidgets
from . import design


class Scene(QGraphicsScene):
    def wheelEvent(self, event):
        if event.delta() > 0:
            ComConfig.scale += 0.1
        if event.delta() < 0:
            ComConfig.scale -= 0.1


class InterApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, client: Client):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.connectButton.clicked.connect(self.connect)
        self.new_world.clicked.connect(lambda: self.show_frame('world_frame', self.new_world_setting))
        self.create_button.clicked.connect(self.create_world)
        self.delete_button.clicked.connect(self.delete_world)
        self.play_button.clicked.connect(self.start_game)

        self.scene = Scene()
        self.canvas.setScene(self.scene)

    def start_game(self):
        self.client.game = Game([], )
        data = self.world_selection.currentData()
        if data is None:
            QtWidgets.QMessageBox(self, text="Выберите мир").show()
            return
        with new_session() as session:
            chunks = session.query(model.Chunk).filter(model.Chunk.world_id == data).all()
        draw_chunks(self.scene, chunks, ComConfig.scale)
        self.show_frame("game_frame")

    def delete_world(self):
        data = self.world_selection.currentData()
        self.client.state.execute("delete_world", {"id": data, "owner": self.client.user.user_id})
        self.load_worlds()

    def create_world(self):
        self.client.state.execute("create_world",
                                  {"name": self.world_name.text(),
                                   "type": "ground",
                                   "private": self.world_private.isChecked(),
                                   "owner": self.client.user.user_id,
                                   "size": self.switch_size.currentData()})
        self.show_frame("idle_frame", self.load_worlds)

    def new_world_setting(self):
        self.switch_size.clear()
        for key, val in ComConfig.world_size.items():
            self.switch_size.addItem(key, val)

    def connect(self):
        host = self.hostEntry.text()
        port = int(self.portEntry.text())
        if self.client.connect(host, port, Config.id, Config.port):
            self.client.set_state(IdleState)
            self.show_frame('idle_frame', on_load=self.load_worlds)
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
        self.world_selection.clear()
        for world in self.client.state.execute("get_world"):
            self.world_selection.addItem(world['name'], world['id'])


def run_interface(client):
    app = QtWidgets.QApplication(sys.argv)
    window = InterApp(client)
    window.show()
    window.show_frame('connection_frame')
    app.exec_()
