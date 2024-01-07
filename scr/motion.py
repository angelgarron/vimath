from base import RegisterAction
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
            previousLineEdit.setCursorPosition(len(previousLineEdit.text()))
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
        self.key = [[Qt.Key_L], [Qt.Key_Right]]

    
    def performAction(self, other):
        nextLineEdit = other.nextLineEdit
        if other.cursorPosition() == len(other.text()) and nextLineEdit:
            nextLineEdit.setFocus()
            nextLineEdit.setCursorPosition(0)
            return
        other.cursorForward(False)
        

@RegisterAction("insert")
class MoveRightInsert(MoveRight):
    def __init__(self):
        self.key = [Qt.Key_Right]


@RegisterAction(["normal", "visual"])
class MoveWordBegin:
    def __init__(self):
        self.key = [Qt.Key_W]
        
    
    def performAction(self, other):
        nextLineEdit = other.nextLineEdit
        if nextLineEdit is not None:
            nextLineEdit.setFocus()
            nextLineEdit.setCursorPosition(0)
        
        
@RegisterAction(["normal", "visual"])
class MoveBeginningWord:
    def __init__(self):
        self.key = [Qt.Key_B]


    def performAction(self, other):
        previousLineEdit = other.previousLineEdit
        if previousLineEdit is not None:
            previousLineEdit.setFocus()
            previousLineEdit.setCursorPosition(0)
        


@RegisterAction(["normal", "visual"])
class MoveWordEnd:
    def __init__(self):
        self.key = [Qt.Key_E]

    
    def performAction(self, other):
        nextLineEdit = other.nextLineEdit
        if nextLineEdit is not None:
            nextLineEdit.setFocus()
            nextLineEdit.setCursorPosition(len(nextLineEdit.text()))        
            return
        other.setCursorPosition(len(other.text()))        


@RegisterAction(["normal", "visual"])
class MoveStartDocument:
    def __init__(self):
        self.key = [Qt.Key_G, Qt.Key_G]

        
    def performAction(self, other):
        firstLine = scene.window.mainMathFrame.children[0].firstLineEdit
        firstLine.setFocus()
        firstLine.setCursorPosition(0)


@RegisterAction(["normal", "visual"])
class MoveEndDocument:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_G]


    def performAction(self, other):
        lastLine = scene.window.mainMathFrame.children[-1].firstLineEdit
        lastLine.setFocus()
        lastLine.setCursorPosition(0)


@RegisterAction(["normal", "visual"])
class MoveStartOfLine:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Underscore]
    

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
