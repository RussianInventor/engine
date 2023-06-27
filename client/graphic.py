from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
scene = QGraphicsScene(x=0, y=0, width=100, height=120)
scene.addRect(x=100, y=10, w=25, h=35, pen=QPen(Qt.PenStyle.SolidLine))
