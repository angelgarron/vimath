from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import Qt, QSize

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


class MyLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyle(ThickCursorStyle())
        self.setStyleSheet(LINEDIT_STYLESHEET)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setFont(QFont("monospace", self.parent.fontSize))
        self.storedKeys = []
        self.scene = self.parent.scene
        self.scene.addLineEdit(self)
        self.u = self.parent.fontSize/2+2
        self.d = self.parent.fontSize/2+2
        self.setGeometry(0, 0, LINEDIT_SIZE[0], self.u+self.d)
        self.textChanged.connect(self.updateWidth)
        self.textEdited.connect(self.wasEdited)
        self.nextLinedit = None
        self.previousLinedit = None
        self.upperLinedit = None
        self.lowerLinedit = None
        self.updateWidth()
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
        self.scene.updateFrames()
    

    def createFrameMiddle(self, FrameConstructor):
        cursorPosition = self.cursorPosition()
        newFrame = FrameConstructor(self.parent)
        currentLineditPosition = self.parent.children.index(self)
        self.parent.children.insert(currentLineditPosition, newFrame)
        newLinedit = MyLineEdit(self.parent)
        self.parent.children.insert(currentLineditPosition, newLinedit)
        newLinedit.setText(self.text()[:cursorPosition])
        self.setText(self.text()[cursorPosition:])
        newFrame.createLinks(newLinedit, self)
        newFrame.firstLinedit.setFocus()
        newFrame.show()
        self.scene.updateFrames()
        return newFrame
        

    def wheelEvent(self, event):
        print(self)
        return super().wheelEvent(event)


    def keyPressEvent(self, event):
        if event.keyCombination() == Qt.ControlModifier | Qt.Key_C:
            self.storedKeys = []
            if not self.scene.isNormalMode():
                self.cursorBackward(False)
                self.scene.enterNormalMode()
            return

        if self.scene.isInsertMode():
            super().keyPressEvent(event)
            return

        if self.scene.isNormalMode():
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
