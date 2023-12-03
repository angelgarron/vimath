from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import QRect, Qt, QSize
from math_editor_lineedit import MyLineEdit
from math_editor_graphics_frame import MyGraphicsFrame


class MyFrame:
    def __init__(self, parent):
        self.parent = parent
        self.scene = parent.scene
        try:
            self.graphicsFrame = MyGraphicsFrame(self, self.parent.graphicsFrame)
        except AttributeError:
            self.graphicsFrame = MyGraphicsFrame(self, self.parent)
        self.children = []
        self.scene.addFrame(self)
        self.firstLinedit = self.createLineEdit()

        
    def createFrameMiddle(self, currentLinedit, FrameConstructor):
        cursorPosition = currentLinedit.graphicsLineEdit.cursorPosition()
        newFrame = FrameConstructor(self.graphicsFrame)
        currentLineditPosition = self.children.index(currentLinedit)
        self.children.insert(currentLineditPosition, newFrame)
        newLinedit = self.createLineEdit(currentLineditPosition)
        newLinedit.graphicsLineEdit.setText(currentLinedit.graphicsLineEdit.text()[:cursorPosition])
        currentLinedit.graphicsLineEdit.setText(currentLinedit.graphicsLineEdit.text()[cursorPosition:])
        newFrame.createLinks(newLinedit, currentLinedit)
        newFrame.firstLinedit.graphicsLineEdit.setFocus()
        return newFrame
        

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
        
        self.graphicsFrame.setGeometry(QRect(self.graphicsFrame.x(), self.graphicsFrame.y(), width, self.u+self.d))
    

    def createLineEdit(self):
        newLinedit = MyLineEdit(self)
        return newLinedit
    