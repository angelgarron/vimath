from base import RegisterAction, BaseMovement
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import Qt

@RegisterAction
class MoveLeft(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_H]
        self.movement = QTextCursor.MoveOperation.PreviousCharacter

@RegisterAction
class MoveDown(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_J]
        self.movement = QTextCursor.MoveOperation.Down

@RegisterAction
class MoveUp(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_K]
        self.movement = QTextCursor.MoveOperation.Up
        
@RegisterAction
class MoveRight(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_L]
        self.movement = QTextCursor.MoveOperation.Right

@RegisterAction
class MoveWordBegin(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_W]
        self.movement = QTextCursor.MoveOperation.NextWord
        
        
@RegisterAction
class MoveBeginningWord(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_B]
        self.movement = QTextCursor.MoveOperation.PreviousWord

@RegisterAction
class MoveWordEnd(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_E]
        self.movement = [
    QTextCursor.MoveOperation.NextWord, 
    QTextCursor.MoveOperation.EndOfWord, 
    #  QTextCursor.MoveOperation.PreviousCharacter
    ]