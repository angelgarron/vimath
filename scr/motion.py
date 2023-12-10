from base import RegisterAction
from scene import scene
from PySide6.QtGui import Qt


@RegisterAction("both")
class MoveLeft:
    def __init__(self):
        self.key = [[Qt.Key_H], [Qt.Key_Left]]

        
    def performAction(self, other):
        if other.cursorPosition() == 0 and other.previousLinedit:
            other.previousLinedit.setFocus()
            other.previousLinedit.setCursorPosition(len(other.previousLinedit.text()))
            return
        other.cursorBackward(scene.isVisualMode())


class MoveVertical:
    def giveFocusProportion(self, lineEdit, elements):
        cursorPosition = lineEdit.cursorPosition()
        if len(lineEdit.text()) > 0:
            prop = cursorPosition/len(lineEdit.text())
        else:
            prop = 0.5
        pos = round((len(elements)-1)*prop)
        elements[pos].setFocus()


@RegisterAction("both")
class MoveDown(MoveVertical):
    def __init__(self):
        self.key = [[Qt.Key_J], [Qt.Key_Down]]
        
        
    def performAction(self, other):
        if other.lowerLinedit:
            denominatorElements = other.lowerLinedit.parent.children
            self.giveFocusProportion(other, denominatorElements)


@RegisterAction("both")
class MoveUp(MoveVertical):
    def __init__(self):
        self.key = [[Qt.Key_K], [Qt.Key_Up]]

        
    def performAction(self, other):
        if other.upperLinedit:
            numeratorElements = other.upperLinedit.parent.children
            self.giveFocusProportion(other, numeratorElements)
        

@RegisterAction("both")
class MoveRight:
    def __init__(self):
        self.key = [[Qt.Key_L], [Qt.Key_Right]]

    
    def performAction(self, other):
        if other.cursorPosition() == len(other.text()) and other.nextLinedit:
            other.nextLinedit.setFocus()
            other.nextLinedit.setCursorPosition(0)
            return
        other.cursorForward(scene.isVisualMode())
        

@RegisterAction("both")
class MoveWordBegin:
    def __init__(self):
        self.key = [Qt.Key_W]
        
    
    def performAction(self, other):
        other.cursorWordForward(scene.isVisualMode())
        
        
@RegisterAction("both")
class MoveBeginningWord:
    def __init__(self):
        self.key = [Qt.Key_B]


    def performAction(self, other):
        other.cursorWordBackward(scene.isVisualMode())


@RegisterAction("both")
class MoveWordEnd:
    # FIXME
    def __init__(self):
        self.key = [Qt.Key_E]

    
    def performAction(self, other):
        movements = [
                    other.cursorWordForward, 
                    other.cursorWordForward, 
                    other.cursorBackward, 
                    other.cursorBackward, 
                    ]

        for movement in movements:
            movement(scene.isVisualMode())
        


@RegisterAction("both")
class MoveStartDocument:
    def __init__(self):
        self.key = [Qt.Key_G, Qt.Key_G]

        
    def performAction(self, other):
        other.home(scene.isVisualMode())


@RegisterAction("both")
class MoveEndDocument:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_G]


    def performAction(self, other):
        other.end(scene.isVisualMode())


@RegisterAction("both")
class MoveStartOfLine:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Underscore]
    

    def performAction(self, other):
        previousLinedit = other
        while previousLinedit.previousLinedit:
            previousLinedit = previousLinedit.previousLinedit
        previousLinedit.home(False)
        previousLinedit.setFocus()


@RegisterAction("both")
class MoveEndOfLine:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Dollar]


    def performAction(self, other):
        nextLinedit = other
        while nextLinedit.nextLinedit:
            nextLinedit = nextLinedit.nextLinedit
        nextLinedit.end(False)
        nextLinedit.setFocus()
