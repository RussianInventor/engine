from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene

chunk_color = {"field": (0, 200, 0),
               "mountains": (100, 100, 0),
               "beach": (0, 200, 200),
               "water": (50, 200, 50),
               "desert": (200, 0, 0),
               "MEGA_MOUNTAINS": (0, 0, 0)
               }


def draw_chunks(scene: QGraphicsScene, chunks):
    for chu in chunks:
        scene.addRect(chu.x*10, chu.y*10, 10, 10,
                      pen=QPen(Qt.PenStyle.SolidLine),
                      brush=QBrush(Qt.BrushStyle.SolidPattern))


def test(scene: QGraphicsScene):
    scene.addRect(100, 10, 25, 35,
                  pen=QPen(Qt.PenStyle.SolidLine),
                  brush=QBrush(Qt.BrushStyle.CrossPattern))

