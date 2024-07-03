from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from vimath.lineedit import MyLineEdit
from vimath.scene import scene


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
        self.pen = QPen()
        self.pen.setColor("black")
        self.children = []
        self.show()

        
    def getFontSize(self):
        fontSize = self.parent.fontSize
        return fontSize


    def setFirstLineEdit(self):
        firstLineEdit = MyLineEdit(self)
        self.children.append(firstLineEdit)

        
    @property
    def firstLineEdit(self):
        return self.children[0]
    

    @property
    def lastLineEdit(self):
        return self.children[-1]


    @property
    def nextLineEdit(self):
        if self == self.scene.window.mainMathFrame:
            return None
        indx = self.parent.children.index(self)+1
        try:
            return self.parent.children[indx]
        except IndexError: # we were in the last element of the frame
            return self.parent.nextLineEdit


    @property
    def previousLineEdit(self):
        if self == self.scene.window.mainMathFrame:
            return None
        indx = self.parent.children.index(self)-1
        if indx == -1: # we were in the first element of the frame
            return self.parent.previousLineEdit
        return self.parent.children[indx]


    @property
    def upperLineEdit(self):
        if self == self.scene.window.mainMathFrame:
            return None
        return self.parent.upperLineEdit
    

    @property
    def lowerLineEdit(self):
        if self == self.scene.window.mainMathFrame:
            return None
        return self.parent.lowerLineEdit
            
            
    def removeFrame(self):
        self.deleteLater()
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
        rightLineEdit.deleteLater()
        self.parent.children.remove(self)
        self.scene.updateFrames()


    def removeChildrenRecursevly(self, element):
        for child in element.children:
            child.deleteLater()
            if not isinstance(child, MyLineEdit):
                self.removeChildrenRecursevly(child)
        

    def updateFrameSizeAndPosition(self):
        self.u = 0
        self.d = 0
        for child in self.children:
            if isinstance(child, MyLineEdit):
                child.updateWidth()
            else:
                child.updateFrameSizeAndPosition()
            self.u = max(self.u, child.u)
            self.d = max(self.d, child.d)
            
        width = 0
        for child in self.children:
            child.setGeometry(width, self.u-child.u, child.width(), child.height())
            width += child.width()
        
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
    

    def setFocus(self):
        self.firstLineEdit.setFocus()

        
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
