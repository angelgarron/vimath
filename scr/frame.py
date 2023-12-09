from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import QRect, Qt, QSize
from lineedit import MyLineEdit

LINEDIT_SIZE = (8, 20)
CURSOR_WIDTH = 12


class BaseFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.scene = parent.scene
        self.u = 0
        self.d = 0
        self.setGeometry(QRect(0, 0, LINEDIT_SIZE[0], LINEDIT_SIZE[1]))
        self.fontSize = self.scene.fontSize
        self.setFont(QFont("monospace", self.fontSize))
        self.setStyleSheet("border:1px dashed red")
        self.pen = QPen()
        self.pen.setColor("black")
        self.children = []
        self.scene.addFrame(self)

        
    def wheelEvent(self, event):
        print(self)
        return super().wheelEvent(event)


    def removeFrame(self):
        self.scene.removeFrame(self)
        indexDeleted = self.parent.children.index(self)
        leftLinedit = self.parent.children[indexDeleted-1]
        rightLinedit = self.parent.children[indexDeleted+1]
        leftText = leftLinedit.text()
        rightText = rightLinedit.text()
        mergedText = leftText+rightText
        rightLinedit.setText(mergedText)
        # give focus to someone else so it doesn't crash when self is deleted
        rightLinedit.setFocus()
        rightLinedit.setCursorPosition(len(leftText))
        rightLinedit.previousLinedit = leftLinedit.previousLinedit
        self.parent.children.remove(leftLinedit)
        self.scene.removeLineEdit(leftLinedit)
        leftLinedit.deleteLater()
        self.parent.children.remove(self)
        self.deleteLater()
        return rightLinedit


    def createLinks(self, newLinedit, currentLinedit):
        newLinedit.previousLinedit = currentLinedit.previousLinedit
        currentLinedit.previousLinedit = self.firstLinedit
        self.firstLinedit.nextLinedit = currentLinedit
        self.firstLinedit.previousLinedit = newLinedit
        newLinedit.nextLinedit = self.firstLinedit


    def updateFrameSizeAndPosition(self):
        self.u = 0
        self.d = 0
        for child in self.children:
            if not isinstance(child, MyLineEdit):
                child.updateFrameSizeAndPosition()
            self.u = max(self.u, child.u)
            self.d = max(self.d, child.d)
            
        width = 0
        x = 0
        for child in self.children:
            child.setGeometry(QRect(x, self.u-child.u, child.width(), child.height()))
            width += child.width()
            x += child.width()
        
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
    

    def createPainter(self):
        painter = QPainter(self)
        painter.setPen(self.pen)
        return painter


class MyFrame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.firstLinedit = MyLineEdit(self)
        self.children.append(self.firstLinedit)
