from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from lineedit import MyLineEdit
from scene import scene


LINEDIT_SIZE = (8, 20)
CURSOR_WIDTH = 12


class BaseFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.scene = parent.scene
        self.u = 0
        self.d = 0
        self.setGeometry(0, 0, LINEDIT_SIZE[0], LINEDIT_SIZE[1])
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
        self.deleteLater()
        self.scene.removeFrame(self)
        self.removeChildrenRecursevly(self)
        indexDeleted = self.parent.children.index(self)
        leftLineEdit = self.parent.children[indexDeleted-1]
        rightLineEdit = self.parent.children[indexDeleted+1]
        leftText = leftLineEdit.text()
        rightText = rightLineEdit.text()
        mergedText = leftText+rightText
        rightLineEdit.setText(mergedText)
        # give focus to someone else so it doesn't crash when self is deleted
        rightLineEdit.setFocus()
        rightLineEdit.setCursorPosition(len(leftText))
        rightLineEdit.previousLinedit = leftLineEdit.previousLinedit
        self.parent.children.remove(leftLineEdit)
        self.scene.removeLineEdit(leftLineEdit)
        leftLineEdit.deleteLater()
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
        


    def createLinks(self, newLinedit, currentLinedit):
        newLinedit.previousLinedit = currentLinedit.previousLinedit
        currentLinedit.previousLinedit = self.firstLinedit
        self.firstLinedit.nextLinedit = currentLinedit
        self.firstLinedit.previousLinedit = newLinedit
        newLinedit.nextLinedit = self.firstLinedit

        # the links that before were pointing to currentLinedit
        # should now point to newLinedit
        # find the element to the left to rearrange those links
        element = self.findElementLeft(newLinedit)
        if element is not None:
            self.rearrangeLinks(element, newLinedit)

        
    def findElementLeft(self, currentElement):
        # check if currentElement is a denominator frame so it doesn't go from numerator to denominator
        if hasattr(currentElement.parent, "denominator"):
            if currentElement.parent.denominator == currentElement:
                return
        # don't keep looking if we reached parent window
        if scene.window == currentElement.parent:
            return
        indx = currentElement.parent.children.index(currentElement)-1
        if indx == -1: # meaning that we do not have anything to the left
            return self.findElementLeft(currentElement.parent)
        element = currentElement.parent.children[indx]
        return element

        
    def rearrangeLinks(self, element, newLinedit):
        """Make all the nextLinedit inside `element` (recursively) point to newLinedit
        """
        if not isinstance(element, MyLineEdit):
            for child in element.children:
                self.rearrangeLinks(child, newLinedit)
        else:
            element.nextLinedit = newLinedit


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


class MyFrame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.firstLinedit = MyLineEdit(self)
        self.children.append(self.firstLinedit)
