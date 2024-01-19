from base import RegisterAction
from constructors import Parenthesis
from scene import scene
from PySide6.QtGui import Qt


@RegisterAction(["normal", "visual"])
class MoveLeft:
    def __init__(self):
        self.key = [[Qt.Key_H], [Qt.Key_Left]]

        
    def performAction(self, other):
        previousLineEdit = other.previousLineEdit
        if other.cursorPosition() == 0 and previousLineEdit:
            previousLineEdit.setFocus()
            previousLineEdit.end(False)
            return
        other.cursorBackward(False)

        
@RegisterAction("insert")
class MoveLeftInsert(MoveLeft):
    def __init__(self):
        self.key = [Qt.Key_Left]


class MoveVertical:
    def giveFocusProportion(self, lineEdit, elements):
        cursorPosition = lineEdit.cursorPosition()
        if len(lineEdit.text()) > 0:
            prop = cursorPosition/len(lineEdit.text())
        else:
            prop = 0.5
        pos = round((len(elements)-1)*prop)
        elements[pos].setFocus()


@RegisterAction(["normal", "visual"])
class MoveDown(MoveVertical):
    def __init__(self):
        self.key = [[Qt.Key_J], [Qt.Key_Down]]
        
        
    def performAction(self, other):
        if other.lowerLineEdit:
            denominatorElements = other.lowerLineEdit.parent.children
            self.giveFocusProportion(other, denominatorElements)


@RegisterAction("insert")
class MoveDownInsert(MoveDown):
    def __init__(self):
        self.key = [Qt.Key_Down]


@RegisterAction(["normal", "visual"])
class MoveUp(MoveVertical):
    def __init__(self):
        self.key = [[Qt.Key_K], [Qt.Key_Up]]

        
    def performAction(self, other):
        if other.upperLineEdit:
            numeratorElements = other.upperLineEdit.parent.children
            self.giveFocusProportion(other, numeratorElements)
        

@RegisterAction("insert")
class MoveUpInsert(MoveUp):
    def __init__(self):
        self.key = [Qt.Key_Up]


@RegisterAction(["normal", "visual"])
class MoveRight:
    def __init__(self):
        self.key = [[Qt.Key_L], [Qt.Key_Right], [Qt.Key_Space]]

    
    def performAction(self, other):
        nextLineEdit = other.nextLineEdit
        if other.cursorPosition() == len(other.text()) and nextLineEdit:
            nextLineEdit.setFocus()
            nextLineEdit.home(False)
            return
        other.cursorForward(False)
        

@RegisterAction("insert")
class MoveRightInsert(MoveRight):
    def __init__(self):
        self.key = [[Qt.Key_Right], [Qt.Key_Space]]


@RegisterAction(["normal", "insert"])
class MoveRightExitParenthesis(MoveRight):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_ParenRight]

        
    def performAction(self, other):
        if other.cursorPosition() == len(other.text()) and isinstance(other.parent.parent, Parenthesis):
            super().performAction(other)


@RegisterAction(["normal", "visual"])
class MoveWordBegin:
    def __init__(self):
        self.key = [Qt.Key_W]
        
    
    def performAction(self, other):
        nextLineEdit = other.nextLineEdit
        if nextLineEdit is not None:
            nextLineEdit.setFocus()
            nextLineEdit.home(False)
        
        
@RegisterAction(["normal", "visual"])
class MoveBeginningWord:
    def __init__(self):
        self.key = [Qt.Key_B]


    def performAction(self, other):
        previousLineEdit = other.previousLineEdit
        if previousLineEdit is not None:
            previousLineEdit.setFocus()
            previousLineEdit.home(False)
        


@RegisterAction(["normal", "visual"])
class MoveWordEnd:
    def __init__(self):
        self.key = [Qt.Key_E]

    
    def performAction(self, other):
        nextLineEdit = other.nextLineEdit
        if nextLineEdit is not None:
            nextLineEdit.setFocus()
            nextLineEdit.end(False)
            return
        other.end(False)


@RegisterAction(["normal", "visual"])
class MoveStartDocument:
    def __init__(self):
        self.key = [Qt.Key_G, Qt.Key_G]

        
    def performAction(self, other):
        firstLine = scene.window.mainMathFrame.children[0].firstLineEdit
        firstLine.setFocus()
        firstLine.home(False)


@RegisterAction(["normal", "visual"])
class MoveEndDocument:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_G]


    def performAction(self, other):
        lastLine = scene.window.mainMathFrame.children[-1].firstLineEdit
        lastLine.setFocus()
        lastLine.home(False)


@RegisterAction(["normal", "visual"])
class MoveStartOfLine:
    def __init__(self):
        self.key = [Qt.Key_0]
    

    def performAction(self, other):
        previousLineEdit = other
        while previousLineEdit.previousLineEdit:
            previousLineEdit = previousLineEdit.previousLineEdit
        previousLineEdit.home(False)
        previousLineEdit.setFocus()


@RegisterAction(["normal", "visual"])
class MoveEndOfLine:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Dollar]


    def performAction(self, other):
        nextLineEdit = other
        while nextLineEdit.nextLineEdit:
            nextLineEdit = nextLineEdit.nextLineEdit
        nextLineEdit.end(False)
        nextLineEdit.setFocus()
