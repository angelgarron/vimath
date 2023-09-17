from base import RegisterAction, BaseMovement
from PySide6.QtGui import Qt


@RegisterAction("both")
class MoveLeft(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_H], [Qt.Key_Left]]

        
    def performAction(self, other):
        if other.cursorPosition() == 0 and other.previousLinedit:
            other.previousLinedit.setFocus()
            return
        other.cursorBackward(self.checkmark(other))


@RegisterAction("both")
class MoveDown(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_J], [Qt.Key_Down]]
        
        
    def performAction(self, other):
        if other.lowerLinedit:
            other.lowerLinedit.setFocus()


@RegisterAction("both")
class MoveUp(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_K], [Qt.Key_Up]]

        
    def performAction(self, other):
        if other.upperLinedit:
            other.upperLinedit.setFocus()
        

@RegisterAction("both")
class MoveRight(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_L], [Qt.Key_Right]]

    
    def performAction(self, other):
        if other.cursorPosition() == len(other.text()) and other.nextLinedit:
            other.nextLinedit.setFocus()
            return
        other.cursorForward(self.checkmark(other))
        

@RegisterAction("both")
class MoveWordBegin(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_W]
        
    
    def performAction(self, other):
        other.cursorWordForward(self.checkmark(other))
        
        
@RegisterAction("both")
class MoveBeginningWord(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_B]


    def performAction(self, other):
        other.cursorWordBackward(self.checkmark(other))


@RegisterAction("both")
class MoveWordEnd(BaseMovement):
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
            movement(self.checkmark(other))
        


@RegisterAction("both")
class MoveStartDocument(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_G, Qt.Key_G]

        
    def performAction(self, other):
        other.home(self.checkmark(other))


@RegisterAction("both")
class MoveEndDocument(BaseMovement):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_G]


    def performAction(self, other):
        other.end(self.checkmark(other))


@RegisterAction("both")
class MoveStartOfLine(BaseMovement):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Underscore]
    

    def performAction(self, other):
        other.home(self.checkmark(other))


@RegisterAction("both")
class MoveEndOfLine(BaseMovement):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Dollar]


    def performAction(self, other):
        other.end(self.checkmark(other))
