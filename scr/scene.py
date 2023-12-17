from PySide6.QtWidgets import QProxyStyle
from PySide6.QtCore import QPoint
from lineedit import ThickCursorStyle, MyLineEdit

NORMAL_MODE = 0
INSERT_MODE = 1
VISUAL_MODE = 2

class Scene:
    def __init__(self):
        self.fontSize = 15
        self.mode = NORMAL_MODE
        self.frames = []
        self.lineEdits = []
        self.storedKeys = []
        self.selectionFirst = None
        self.selectionSecond = None
        self.selection = []

        
    def getLineEditWithFocus(self):
        return self.window.focusWidget()


    def lookdowntree(self, element, secondelement):
        if isinstance(element, MyLineEdit):
            if element == secondelement:
                return element
            return
        for child in element.children:
            element = self.lookdowntree(child, secondelement)
            if element:
                return element


    def lookuptree(self, firstelement, secondelement, currentbranch):
        for child in currentbranch.parent.children:
            if child != currentbranch:
                element = self.lookdowntree(child, secondelement)
                if element:
                    start = currentbranch.parent.children.index(currentbranch)
                    end = currentbranch.parent.children.index(child)
                    if start>end:
                        start, end = end, start
                    for i in range(start, end+1):
                        self.selection.append(currentbranch.parent.children[i])
                    return element
        return self.lookuptree(firstelement, secondelement, currentbranch.parent)

        
    def updateVisualSelection(self):
        print("updating visual selection")
        lineEditWithFocus = self.getLineEditWithFocus()
        self.selectionSecond = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]
        print("selectionFirst", self.selectionFirst)
        print("selectionSecond", self.selectionSecond)
        self.selection = []
        if self.selectionFirst[0] == self.selectionSecond[0]:
            self.selection.append(self.selectionFirst[0])
            print("same lineEdit")
        else:
            element = self.lookuptree(self.selectionFirst[0], self.selectionSecond[0], self.selectionFirst[0])
            print(element)
        print("the selection is", self.selection)
        self.setSelectionGeometry()


    def clearSelection(self):
        print("clearing selection")
        self.selectionFirst = None
        self.selectionSecond = None
        self.window.tp.hide()


    def startSelection(self):
        print("adding selection first and second")
        lineEditWithFocus = self.getLineEditWithFocus()
        self.selectionFirst = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]
        self.selectionSecond = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]
        self.window.tp.show()


    def getAbsolutePosition(self, element, pos):
        pos += element.pos()
        if element.parent == self.window:
            return pos
        return self.getAbsolutePosition(element.parent, pos)

        
    def setSelectionGeometry(self):
        if self.selection:
            width = 0
            for element in self.selection[:-1]:
                width += element.width()
            x = self.selection[0].x()
            x += self.selectionFirst[1]*12
            width += self.selectionSecond[1]*12
            width -= x
            print("x, width", x, width)
            pos = self.getAbsolutePosition(self.selection[0].parent, QPoint(x, 0))
            self.window.tp.setGeometry(pos.x(), pos.y(), width, self.selection[0].parent.height())


    def updateFrames(self):
        mainFrame = self.frames[0]
        mainFrame.updateFrameSizeAndPosition()


    def addFrame(self, frame):
        self.frames.append(frame)
    

    def addLineEdit(self, lineEdit):
        self.lineEdits.append(lineEdit)
    

    def removeFrame(self, frame):
        self.frames.remove(frame)
    

    def removeLineEdit(self, lineEdit):
        self.lineEdits.remove(lineEdit)

        
    def enterInsertMode(self):
        self.mode = INSERT_MODE
        for lineEdit in self.lineEdits:
            lineEdit.setStyle(QProxyStyle())


    def enterNormalMode(self):
        if self.isVisualMode():
            self.clearSelection()
        self.mode = NORMAL_MODE
        for lineEdit in self.lineEdits:
            lineEdit.setStyle(ThickCursorStyle())


    def enterVisualMode(self):
        self.mode = VISUAL_MODE
        self.startSelection()
        for lineEdit in self.lineEdits:
            lineEdit.setStyle(ThickCursorStyle())

            
    def isNormalMode(self):
        return self.mode == NORMAL_MODE
    

    def isInsertMode(self):
        return self.mode == INSERT_MODE
    

    def isVisualMode(self):
        return self.mode == VISUAL_MODE


scene = Scene()
# initialize all actions
import motion, operators, addconstructor
from base import actions, actionsVisual, actionsInsert
scene.actions = actions
scene.actionsVisual = actionsVisual
scene.actionsInsert = actionsInsert
