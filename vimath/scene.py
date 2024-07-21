import json
from PySide6.QtCore import QPoint
from vimath.lineedit import  MyLineEdit
from vimath.clipboard import Clipboard
from vimath.history import History
from enum import Enum, auto


class Mode(Enum):
    NORMAL = auto()
    INSERT = auto()
    VISUAL = auto()


class Scene:
    def __init__(self):
        self.fontSize = 15
        self.mode = Mode.NORMAL
        self.storedKeys = []
        self.selectionFirst = None
        self.selectionSecond = None
        self.selection = []
        self.clipboard = Clipboard(self)
        self.history = History(self)

        
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
        lineEditWithFocus = self.getLineEditWithFocus()
        self.selectionSecond = [lineEditWithFocus, lineEditWithFocus.cursorPosition()]
        self.selection = []
        if self.selectionFirst[0] == self.selectionSecond[0]:
            if self.selectionFirst[1]>self.selectionSecond[1]:
                self.selection.append((self.selectionSecond[0], self.selectionSecond[1]))
                self.selection.append((self.selectionFirst[0], self.selectionFirst[1]))
            else:
                self.selection.append((self.selectionFirst[0], self.selectionFirst[1]))
                self.selection.append((self.selectionSecond[0], self.selectionSecond[1]))
        else:
            element = self.lookuptree(self.selectionFirst[0])
        self.setSelectionGeometry()


    def clearSelection(self):
        self.selectionFirst = None
        self.selectionSecond = None
        self.window.tp.hide()


    def startSelection(self):
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
                start = self.selection[0][0].x()+\
                self.selection[0][0].getDimensionUntilCursorPosition(self.selection[0][1])[0]
            else:
                start = self.selection[0][0].x()
            if self.selection[-1][1] is not None:
                end = self.selection[-1][0].x()+\
                self.selection[-1][0].getDimensionUntilCursorPosition(self.selection[-1][1])[0]
            else:
                end = self.selection[-1][0].x()+self.selection[-1][0].width()
            pos = self.getAbsolutePosition(self.selection[0][0].parent, QPoint(start, 0))
            self.window.tp.setGeometry(pos.x(), pos.y(), end-start, self.selection[0][0].parent.height())


    def deleteSelection(self, selection=None, storeHistory=True):
        from vimath import constructors
        if selection is None:
            selection = self.selection

        first = selection[0]
        second = selection[-1]
        if isinstance(first[0], constructors.fraction.Numerator):
            return
        
        if first[0] == second[0]: # we are in the same lineEdit
            first[0].setCursorPosition(first[1])
            first[0].cursorForward(True, second[1]-first[1])
            first[0].deleteText()
            if storeHistory:
                scene.history.store("delete selection")
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
        for i, s in enumerate(selection[start:end]):
            if i%2 != 0:
                s[0].clear()
        # remove the frames inbetween
        for i, s in enumerate(selection[start:end]):
            if i%2 == 0:
                s[0].removeFrame()

        if storeHistory:
            scene.history.store("delete selection")


    def updateFrames(self):
        mainFrame = self.window.mainMathFrame
        mainFrame.updateFrameSizeAndPosition()
        self.window.graphicCursor.updatePosition()


    def enterInsertMode(self):
        self.mode = Mode.INSERT
        self.storedKeys = []
        self.window.updateStatusBar()
        self.window.graphicCursor.updatePosition()


    def enterNormalMode(self):
        if self.isVisualMode():
            self.clearSelection()
        self.mode = Mode.NORMAL
        self.window.updateStatusBar()
        self.window.graphicCursor.updatePosition()


    def enterVisualMode(self):
        self.mode = Mode.VISUAL
        self.startSelection()
        self.window.updateStatusBar()
        self.window.graphicCursor.updatePosition()

            
    def isNormalMode(self):
        return self.mode == Mode.NORMAL
    

    def isInsertMode(self):
        return self.mode == Mode.INSERT
    

    def isVisualMode(self):
        return self.mode == Mode.VISUAL

        
    @property
    def currentMode(self):
        return self.mode.name


    def clear(self):
        """Clear the contents of the scene
        """
        # remove all lines except for the first one
        # the last line will just be cleared
        for line in self.window.mainMathFrame.children.copy():
            line.removeLine()


    def clearLine(self, line):
        # give focus to the base if we have focus on an empty script when clearing
        # this is to avoid the focusOutEvent trying to remove the script before
        lineEditWithFocus = self.getLineEditWithFocus()
        if isinstance(lineEditWithFocus.parent, (
           constructors.subscript.Inferior,
           constructors.superscript.Superior,
           constructors.supersubscript.Superior,
           constructors.supersubscript.Inferior, 
        )) and len(lineEditWithFocus.text()) == 0:
            lineEditWithFocus.parent.parent.base.firstLineEdit.setFocus()

        for element in line.children.copy():
            if not isinstance(element, MyLineEdit):
                element.removeFrame()
        # clear the remaining lineEdit
        line.children[0].clear()
    

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            json.dump(self.serialize(), file, indent=4)


    def loadFromFile(self, filename):
        with open(filename) as file:
            data = json.load(file)
            self.deserialize(data)
        scene.history.store("loaded from file")


    def serialize(self):
        mainFrame = self.window.mainMathFrame
        elements = []
        for element in mainFrame.children:
            elements.append(element.serialize())

        return {
            "mainFrame": elements
        }


    def deserialize(self, data):
        self.clear()
        mainFrame = self.window.mainMathFrame
        mainFrame.deserialize(data["mainFrame"])
        mainFrame.children[0].removeLine()
        self.updateFrames()


scene = Scene()
# initialize all actions
from vimath import motion, operators, addconstructor, symbols
from vimath.base import actions, actionsVisual, actionsInsert
scene.actions = actions
scene.actionsVisual = actionsVisual
scene.actionsInsert = actionsInsert

from vimath.frame import MyFrame
from vimath import constructors

returnClass = {
    "<class 'vimath.lineedit.MyLineEdit'>": MyLineEdit,
    "<class 'vimath.constructors.fraction.Fraction'>": constructors.Fraction,
    "<class 'vimath.frame.MyFrame'>": MyFrame,
    "<class 'vimath.constructors.squareroot.SquareRoot'>": constructors.SquareRoot,
    "<class 'vimath.constructors.parenthesis.Parenthesis'>": constructors.Parenthesis,
    "<class 'vimath.constructors.subscript.Subscript'>": constructors.Subscript,
    "<class 'vimath.constructors.superscript.Superscript'>": constructors.Superscript,
    "<class 'vimath.constructors.supersubscript.SuperSubscript'>": constructors.SuperSubscript,
    "<class 'vimath.constructors.mainframe.Line'>": constructors.mainframe.Line,
}
scene.returnClass = returnClass
