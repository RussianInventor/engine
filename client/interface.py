import subprocess
subprocess.call(("pyuic5",
                 "untitled.ui",
                 "-o",
                 "design.py"))
import sys
from PyQt5 import QtWidgets
import design


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connectButton.clicked.connect(self.connect)

    def connect(self):
        host = self.hostEntry.text()
        port = self.portEntry.text()
        print(host, port)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':\
    main()
