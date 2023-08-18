from base import RegisterAction, BaseMovement, KeyCombination, actions
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import Qt

@RegisterAction("both")
class MoveLeft(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_H], [Qt.Key_Left]]
        self.movement = QTextCursor.MoveOperation.PreviousCharacter

@RegisterAction("both")
class MoveDown(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_J], [Qt.Key_Down]]
        self.movement = QTextCursor.MoveOperation.Down

@RegisterAction("both")
class MoveUp(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_K], [Qt.Key_Up]]
        self.movement = QTextCursor.MoveOperation.Up
        
@RegisterAction("both")
class MoveRight(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_L], [Qt.Key_Right]]
        self.movement = QTextCursor.MoveOperation.Right

@RegisterAction("both")
class MoveWordBegin(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_W]
        self.movement = QTextCursor.MoveOperation.NextWord
        
        
@RegisterAction("both")
class MoveBeginningWord(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_B]
        self.movement = QTextCursor.MoveOperation.PreviousWord

@RegisterAction("both")
class MoveWordEnd(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_E]
        self.movement = [
    QTextCursor.MoveOperation.NextWord, 
    QTextCursor.MoveOperation.EndOfWord, 
    #  QTextCursor.MoveOperation.PreviousCharacter
    ]

@RegisterAction("both")
class MoveStartDocument(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_G, Qt.Key_G]
        self.movement = QTextCursor.MoveOperation.Start

@RegisterAction("both")
class MoveEndDocument(BaseMovement):
    def __init__(self):
        self.key = [KeyCombination(Qt.ShiftModifier, Qt.Key_G)]
        self.movement = QTextCursor.MoveOperation.End

@RegisterAction("both")
class MoveStartOfLine(BaseMovement):
    def __init__(self):
        self.key = [KeyCombination(Qt.ShiftModifier, Qt.Key_Underscore)]
        self.movement = QTextCursor.MoveOperation.StartOfLine

@RegisterAction("both")
class MoveEndOfLine(BaseMovement):
    def __init__(self):
        self.key = [KeyCombination(Qt.ShiftModifier, Qt.Key_Dollar)]
        self.movement = QTextCursor.MoveOperation.EndOfLine
