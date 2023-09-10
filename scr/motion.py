from base import RegisterAction, BaseMovement, actions
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit


@RegisterAction("both")
class MoveLeft(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_H], [Qt.Key_Left]]
        self.movement = QLineEdit.cursorBackward


# @RegisterAction("both")
# class MoveDown(BaseMovement):
#     def __init__(self):
#         self.key = [[Qt.Key_J], [Qt.Key_Down]]
#         self.movement = QTextCursor.MoveOperation.Down

# @RegisterAction("both")
# class MoveUp(BaseMovement):
#     def __init__(self):
#         self.key = [[Qt.Key_K], [Qt.Key_Up]]
#         self.movement = QTextCursor.MoveOperation.Up
        
@RegisterAction("both")
class MoveRight(BaseMovement):
    def __init__(self):
        self.key = [[Qt.Key_L], [Qt.Key_Right]]
        self.movement = QLineEdit.cursorForward


@RegisterAction("both")
class MoveWordBegin(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_W]
        self.movement = QLineEdit.cursorWordForward
        
        
@RegisterAction("both")
class MoveBeginningWord(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_B]
        self.movement = QLineEdit.cursorWordBackward


@RegisterAction("both")
class MoveWordEnd(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_E]
        self.movement = [
    QLineEdit.cursorWordForward, 
    QLineEdit.cursorWordForward, 
    QLineEdit.cursorBackward, 
    QLineEdit.cursorBackward, 
    ]


@RegisterAction("both")
class MoveStartDocument(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_G, Qt.Key_G]
        self.movement = QLineEdit.home


@RegisterAction("both")
class MoveEndDocument(BaseMovement):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_G]
        self.movement = QLineEdit.end


@RegisterAction("both")
class MoveStartOfLine(BaseMovement):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Underscore]
        self.movement = QLineEdit.home


@RegisterAction("both")
class MoveEndOfLine(BaseMovement):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Dollar]
        self.movement = QLineEdit.end
