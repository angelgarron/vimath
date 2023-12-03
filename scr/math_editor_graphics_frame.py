from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import QRect, Qt, QSize

LINEDIT_SIZE = (8, 20)
CURSOR_WIDTH = 12

class MyGraphicsFrame(QFrame):
    def __init__(self, frame, parent):
        super().__init__(parent)
        self.frame = frame
        self.u = 0
        self.d = 0
        self.setGeometry(QRect(0, 0, LINEDIT_SIZE[0], LINEDIT_SIZE[1]))
        self.fontSize = self.frame.scene.fontSize
        self.setFont(QFont("monospace", self.fontSize))
        self.setStyleSheet("border:1px dashed red")
        # self.painter = QPainter(self)
        # pen = QPen()
        # pen.setColor("black")
        # self.painter.setPen(pen)
