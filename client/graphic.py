from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene
from common.config import Config

chunk_color = {"field": (0, 200, 0),
               "mountains": (50, 0, 0),
               "beach": (250, 250, 0),
               "water": (50, 50, 200),
               "desert": (200, 0, 0),
               "MEGA_MOUNTAINS": (0, 0, 0)
               }


def draw_chunks(scene: QGraphicsScene, chunks, scale):
    size = Config.CHUNK_SIZE * scale
    for row in chunks:
        for chu in row:
            scene.addRect(chu.x * size, chu.y * size, size, size,
                          pen=QColor(*chunk_color[chu.biome]),
                          # brush=QBrush(Qt.BrushStyle.SolidPattern))
                          brush=QColor(*chunk_color[chu.biome]))
    scene.update()


def test(scene: QGraphicsScene):
    scene.addRect(100, 10, 25, 35,
                  pen=QPen(Qt.PenStyle.SolidLine),
                  brush=QBrush(Qt.BrushStyle.CrossPattern))
