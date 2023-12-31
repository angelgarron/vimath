from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from lineedit import MyLineEdit
from scene import scene


LINEDIT_SIZE = (8, 20)
CURSOR_WIDTH = 12


class MyFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.scene = parent.scene
        self.u = 0
        self.d = 0
        self.setGeometry(0, 0, LINEDIT_SIZE[0], LINEDIT_SIZE[1])
        self.fontSize = self.getFontSize()
        self.setFont(QFont("monospace", self.fontSize))
        self.setStyleSheet("border:1px dashed red")
        self.pen = QPen()
        self.pen.setColor("black")
        self.children = []
        self.scene.addFrame(self)
        self.show()

        
    def getFontSize(self):
        fontSize = self.parent.fontSize
        return fontSize


    def setFirstLineEdit(self):
        firstLinedit = MyLineEdit(self)
        self.children.append(firstLinedit)

        
    @property
    def firstLinedit(self):
        return self.children[0]
    

    @property
    def lastLinedit(self):
        return self.children[-1]


    @property
    def nextLinedit(self):
        if self == self.scene.frames[0]:
            return None
        indx = self.parent.children.index(self)+1
        try:
            return self.parent.children[indx]
        except IndexError: # we were in the last element of the frame
            return self.parent.nextLinedit


    @property
    def previousLinedit(self):
        if self == self.scene.frames[0]:
            return None
        indx = self.parent.children.index(self)-1
        if indx == -1: # we were in the first element of the frame
            return self.parent.previousLinedit
        return self.parent.children[indx]


    @property
    def upperLinedit(self):
        if self == self.scene.frames[0]:
            return None
        return self.parent.upperLinedit
    

    @property
    def lowerLinedit(self):
        if self == self.scene.frames[0]:
            return None
        return self.parent.lowerLinedit
            
            
    def wheelEvent(self, event):
        print(self)
        return super().wheelEvent(event)

        
    def removeFrame(self):
        self.deleteLater()
        self.scene.removeFrame(self)
        self.removeChildrenRecursevly(self)
        indexDeleted = self.parent.children.index(self)
        leftLineEdit = self.parent.children[indexDeleted-1]
        rightLineEdit = self.parent.children[indexDeleted+1]
        leftText = leftLineEdit.text()
        rightText = rightLineEdit.text()
        mergedText = leftText+rightText
        leftLineEdit.setText(mergedText)
        # give focus to someone else so it doesn't crash when self is deleted
        leftLineEdit.setFocus()
        leftLineEdit.setCursorPosition(len(leftText))
        self.parent.children.remove(rightLineEdit)
        self.scene.removeLineEdit(rightLineEdit)
        rightLineEdit.deleteLater()
        self.parent.children.remove(self)
        self.scene.updateFrames()


    def removeChildrenRecursevly(self, element):
        for child in element.children:
            child.deleteLater()
            if not isinstance(child, MyLineEdit):
                self.scene.removeFrame(child)
                self.removeChildrenRecursevly(child)
            else:
                self.scene.removeLineEdit(child)
        

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
            child.setGeometry(x, self.u-child.u, child.width(), child.height())
            width += child.width()
            x += child.width()
        
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
    

    def createPainter(self):
        painter = QPainter(self)
        painter.setPen(self.pen)
        return painter
    

    def setFocus(self):
        self.firstLinedit.setFocus()

        
    def serialize(self):
        elements = []
        for element in self.children:
            elements.append(element.serialize())

        return {
            "constructor": str(self.__class__),
            "elements": elements,
        }

        
    def deserialize(self, data):
        for element in data:
            constructor = self.scene.returnClass[element["constructor"]]
            if constructor != MyLineEdit:
                newFrame = constructor(self)
                self.children.append(newFrame)
                newFrame.deserialize(element["elements"])
            else:
                newLineEdit = MyLineEdit(self)
                newLineEdit.setText(element["text"])
                self.children.append(newLineEdit)
