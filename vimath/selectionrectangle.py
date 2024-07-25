from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget


class SelectionRectangle(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.hide()


    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.fillRect(self.rect(), QColor(0, 0, 255, 128))
