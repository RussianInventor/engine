import subprocess
from app.app import Client
from client.config import Config
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
        self.client.connect(host, port, Config.id, Config.port)


def run_interface(client):
    app = QtWidgets.QApplication(sys.argv)
    window = InterApp(client)
    window.show()
    app.exec_()
