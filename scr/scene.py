import json
from PySide6.QtWidgets import QProxyStyle
from PySide6.QtCore import QPoint
from lineedit import ThickCursorStyle, MyLineEdit
from clipboard import Clipboard

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
        self.clipboard = Clipboard(self)

        
    def getLineEditWithFocus(self):
        return self.window.focusWidget()


    def lookdowntree(self, element):
        if isinstance(element, MyLineEdit):
            if element == self.selectionSecond[0]:
                return element
            return
        for child in element.children:
            element = self.lookdowntree(child)
            if element:
                return element


    def lookuptree(self, currentbranch):
        for child in currentbranch.parent.children:
            if child != currentbranch:
                element = self.lookdowntree(child)
                if element:
                    start = currentbranch.parent.children.index(currentbranch)
                    end = currentbranch.parent.children.index(child)
                    if start>end:
                        start, end = end, start
                    for i in range(start, end+1):
                        if self.selectionFirst[0] == currentbranch.parent.children[i]:
                            self.selection.append((currentbranch.parent.children[i], self.selectionFirst[1]))
                        elif self.selectionSecond[0] == currentbranch.parent.children[i]:
                            self.selection.append((currentbranch.parent.children[i], self.selectionSecond[1]))
                        else:
                            self.selection.append((currentbranch.parent.children[i], None))
                    return element
        return self.lookuptree(currentbranch.parent)

        
    def updateVisualSelection(self):
        print("updating visual selection")
        lineEditWithFocus = self.getLineEditWithFocus()
        self.selectionSecond = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]
        print("selectionFirst", self.selectionFirst)
        print("selectionSecond", self.selectionSecond)
        self.selection = []
        if self.selectionFirst[0] == self.selectionSecond[0]:
            if self.selectionFirst[1]>self.selectionSecond[1]:
                self.selection.append((self.selectionSecond[0], self.selectionSecond[1]))
                self.selection.append((self.selectionFirst[0], self.selectionFirst[1]))
            else:
                self.selection.append((self.selectionFirst[0], self.selectionFirst[1]))
                self.selection.append((self.selectionSecond[0], self.selectionSecond[1]))
            print("same lineEdit")
        else:
            element = self.lookuptree(self.selectionFirst[0])
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
            if self.selection[0][1] is not None:
                start = self.selection[0][0].x()+self.selection[0][1]*12
            else:
                start = self.selection[0][0].x()
            if self.selection[-1][1] is not None:
                end = self.selection[-1][0].x()+self.selection[-1][1]*12
            else:
                end = self.selection[-1][0].x()+self.selection[-1][0].width()
            pos = self.getAbsolutePosition(self.selection[0][0].parent, QPoint(start, 0))
            self.window.tp.setGeometry(pos.x(), pos.y(), end-start, self.selection[0][0].parent.height())


    def deleteSelection(self):
        first = self.selection[0]
        second = self.selection[-1]
        
        if first[0] == second[0]: # we are in the same lineEdit
            first[0].setCursorPosition(first[1])
            first[0].cursorForward(True, second[1]-first[1])
            first[0].deleteText()
            return

        start, end = 1, -1
        if isinstance(first[0], MyLineEdit):
            first[0].setCursorPosition(first[1])
            first[0].end(True)
            first[0].deleteText()
        else:
            start = 0

        if isinstance(second[0], MyLineEdit):
            second[0].setCursorPosition(second[1])
            second[0].home(True)
            second[0].deleteText()
        else:
            end = None

        # clear the lineEdits inbetween
        for i, s in enumerate(self.selection[start:end]):
            if i%2 != 0:
                s[0].clear()
        # remove the frames inbetween
        for i, s in enumerate(self.selection[start:end]):
            if i%2 == 0:
                s[0].removeFrame()


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


    def clear(self):
        """Clear the contents of the scene
        """
        for element in self.frames[0].children.copy():
            if not isinstance(element, MyLineEdit):
                element.removeFrame()
        self.frames[0].children[0].clear()
    

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            json.dump(self.serialize(), file, indent=4)


    def loadFromFile(self, filename):
        with open(filename) as file:
            data = json.load(file)
            self.deserialize(data)


    def serialize(self):
        mainFrame = self.frames[0]
        elements = []
        for element in mainFrame.children:
            elements.append(element.serialize())

        return {
            "mainFrame": elements
        }


    def deserialize(self, data):
        print("deserializating data", data)
        self.clear()
        mainFrame = self.frames[0]
        lineEdit = mainFrame.children[0]
        lineEdit.setText(data["mainFrame"][0]["text"])

        mainFrame.deserialize(data["mainFrame"][1:])

        self.updateFrames()



scene = Scene()
# initialize all actions
import motion, operators, addconstructor
from base import actions, actionsVisual, actionsInsert
scene.actions = actions
scene.actionsVisual = actionsVisual
scene.actionsInsert = actionsInsert

from frame import MyFrame
from constructors import Fraction, SquareRoot

returnClass = {
    "<class 'lineedit.MyLineEdit'>": MyLineEdit,
    "<class 'constructors.fraction.Fraction'>": Fraction,
    "<class 'frame.MyFrame'>": MyFrame,
    "<class 'constructors.squareroot.SquareRoot'>": SquareRoot,
}
scene.returnClass = returnClass
