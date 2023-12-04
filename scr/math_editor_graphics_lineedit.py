from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import QRect, Qt, QSize

LINEDIT_SIZE = (8, 20)
CURSOR_WIDTH = 12
LINEDIT_STYLESHEET = """
color: black;
border: 1px solid gray;
border-radius: 4px;
background: transparent;
"""

class ThickCursorStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QProxyStyle.PM_TextCursorWidth:
            return CURSOR_WIDTH

        return super().pixelMetric(metric, option, widget)
        

class MyGraphicsLineEdit(QLineEdit):
    def __init__(self, fontSize, lineEdit, parent=None):
        super().__init__(parent)
        self.lineEdit = lineEdit
        self.scene = self.lineEdit.scene
        self.storedKeys = []
        self.fontSize = fontSize
        self.setStyle(ThickCursorStyle())
        self.setStyleSheet(LINEDIT_STYLESHEET)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setFont(QFont("monospace", self.fontSize))
        self.u = self.fontSize/2+2
        self.d = self.fontSize/2+2
        self.setGeometry(QRect(0, 0, LINEDIT_SIZE[0], self.u+self.d))
        self.textChanged.connect(self.updateWidth)
        self.textEdited.connect(self.wasEdited)
        self.show()

        
    def wasEdited(self):
        text = self.text()
        for action in self.scene.actionsInsert.values():
            cursorPosition = text.find(action.key[0])
            if cursorPosition != -1:
                action.performAction(self, cursorPosition, text)


    def updateWidth(self):
        width = self.fontMetrics().horizontalAdvance(self.text())
        self.setFixedWidth(width+8)
        tight = self.fontMetrics().tightBoundingRect(self.text())
        self.setFixedHeight(tight.height()+6)
        self.setTextMargins(0, -tight.top()-self.font().pointSize()-2, 0, 0)
        self.u = -tight.top()
        self.d = self.height()-self.u
        self.setGeometry(self.x(), self.y(), self.width(), self.u+self.d)
        self.lineEdit.scene.updateFrames()
        

    def wheelEvent(self, event):
        print(self)
        return super().wheelEvent(event)


    def keyPressEvent(self, event):
        if event.keyCombination() == Qt.ControlModifier | Qt.Key_C:
            self.storedKeys = []
            if self.scene.mode != 0:
                self.cursorBackward(False)
                self.scene.enterNormalMode()
            return

        if self.scene.mode == 1:
            super().keyPressEvent(event)
            return

        if self.scene.mode == 0:
            actions = self.scene.actions
        else:
            actions = self.scene.actionsVisual

        if event.key() in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]:
            return

        self.storedKeys.append(event.keyCombination())

        for action in actions.values():
            if isinstance(action.key[0], list):
                for key in action.key:
                    if key == self.storedKeys:
                        action.performAction(self)
                        self.storedKeys = []
                        break
            else:
                if action.key == self.storedKeys:
                    action.performAction(self)
                    self.storedKeys = []
                    break


    @property
    def nextLinedit(self):
        return self.lineEdit.nextLinedit


    @property
    def previousLinedit(self):
        return self.lineEdit.previousLinedit


    @property
    def lowerLinedit(self):
        return self.lineEdit.lowerLinedit
    

    @property
    def upperLinedit(self):
        return self.lineEdit.upperLinedit
