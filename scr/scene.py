from PySide6.QtWidgets import QProxyStyle
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
        # if currentbranch.parent == self.window:
        #     return "reached window"
        for child in currentbranch.parent.children:
            if child != currentbranch:
                element = self.lookdowntree(child, secondelement)
                if element:
                    return element
        return self.lookuptree(firstelement, secondelement, currentbranch.parent)

        
    def updateVisualSelection(self):
        print("updating visual selection")
        lineEditWithFocus = self.getLineEditWithFocus()
        self.selectionSecond = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]
        print("selectionFirst", self.selectionFirst)
        print("selectionSecond", self.selectionSecond)
        if self.selectionFirst[0] == self.selectionSecond[0]:
            print("same lineEdit")
            return
        element = self.lookuptree(self.selectionFirst[0], self.selectionSecond[0], self.selectionFirst[0])
        print(element)


    def clearSelection(self):
        print("clearing selection")
        self.selectionFirst = None
        self.selectionSecond = None


    def startSelection(self):
        print("adding selection first and second")
        lineEditWithFocus = self.getLineEditWithFocus()
        self.selectionFirst = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]
        self.selectionSecond = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]


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
