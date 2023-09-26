import logging
import subprocess
from common.config import Config as ComConfig
from client.config import Config
from .client_state import IdleState, GamingState
from .graphic import draw_chunks
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.Qt import QThread
from common import model
from common.game import Game
from client import graphic

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


class GraphicThread(QThread):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        graphic.draw_chunks(scene=self.app.interface.scene,
                            chunks=self.app.game.world.chunks,
                            scale=ComConfig.scale)


class InterApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.connectButton.clicked.connect(self.connect)
        self.new_world.clicked.connect(lambda: self.show_frame('world_frame', self.new_world_setting))
        self.create_button.clicked.connect(self.create_world)
        self.delete_button.clicked.connect(self.delete_world)
        self.play_button.clicked.connect(self.start_game)

        self.graphic_thread = None
        self.scene = Scene()
        self.canvas.setScene(self.scene)

    def start(self):
        self.show()
        self.show_frame('connection_frame')

    def start_game(self):
        world_id = self.world_selection.currentData()
        if world_id is None:
            QtWidgets.QMessageBox(self, text="Выберите мир").show()
            return
        self.app.game = Game(self.app, players=[], world_id=world_id)
        # self.app.state.execute("run_game", kwargs={'world_id': world_id})
        self.app.set_state(GamingState)

        # with new_session() as session:
        #     chunks = session.query(model.Chunk).filter(model.Chunk.world_id == data).all()
        # draw_chunks(self.scene, chunks, ComConfig.scale)
        self.show_frame("game_frame")
        self.graphic_thread = GraphicThread(self.app)
        self.graphic_thread.start()

    def delete_world(self):
        data = self.world_selection.currentData()
        self.app.state.execute("delete_world", {"id": data, "owner": self.app.exchanger.user.user_id})
        self.load_worlds()

    def create_world(self):
        self.app.state.execute("create_world",
                               {"name": self.world_name.text(),
                                "type": "ground",
                                "private": self.world_private.isChecked(),
                                "owner": self.app.exchanger.user.user_id,
                                "size": self.switch_size.currentData()})
        self.show_frame("idle_frame", self.load_worlds)

    def new_world_setting(self):
        self.switch_size.clear()
        for key, val in ComConfig.world_size.items():
            self.switch_size.addItem(key, val)

    def connect(self):
        host = self.hostEntry.text()
        port = int(self.portEntry.text())
        if self.app.exchanger.connect(host, port, Config.id, Config.port):
            self.app.set_state(IdleState)
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
        for world in self.app.state.execute("get_world"):
            self.world_selection.addItem(world['name'], world['id'])


def create_interface(app):
    return InterApp(app)


def create_app():
    return QtWidgets.QApplication(sys.argv)
