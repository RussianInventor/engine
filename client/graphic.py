from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene


def test(scene: QGraphicsScene):
    scene.addRect(100, 10, 25, 35,
                  pen=QPen(Qt.PenStyle.SolidLine),
                  brush=QBrush(Qt.BrushStyle.CrossPattern))

