from PySide6.QtWidgets import QProxyStyle
from lineedit import ThickCursorStyle

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

        
    def printSelection(self):
        print("selectionFirst", self.selectionFirst)
        print("selectionSecond", self.selectionSecond)


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
        self.mode = NORMAL_MODE
        for lineEdit in self.lineEdits:
            lineEdit.setStyle(ThickCursorStyle())


    def enterVisualMode(self):
        self.mode = VISUAL_MODE
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