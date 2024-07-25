from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer


class GraphicalCursor(QWidget):
    def __init__(self, parent, scene):
        super().__init__(parent)
        self.scene = scene
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.blink)
        self.timer.start()
        self.isShowing = True
        
        
    @property
    def cursorWidth(self):
        if self.scene.isInsertMode():
            return 1
        else:
            return self.scene.getLineEditWithFocus().fontSize

        
    def blink(self):
        if self.isShowing:
            self.hide()
            self.isShowing = False
        else:
            self.show()
            self.isShowing = True


    def updatePosition(self):
        self.show()
        lineEditWithFocus = self.scene.getLineEditWithFocus()
        if lineEditWithFocus is not None:
            pos = lineEditWithFocus.geometryCursorPosition
            self.setGeometry(pos.x(), pos.y(), self.cursorWidth, lineEditWithFocus.fontSize*1.2)


    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.fillRect(self.rect(), QColor(0, 0, 0, 50))
