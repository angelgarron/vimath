from base import RegisterAction, BaseMovement, KeyCombination, actions
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import Qt

class BaseInnerWord:
    def performAction(self, other):
        actions["MoveBeginningWord"].performAction(other)
        actions["MoveWordEnd"].performAction(other, moveAnchor=False)
        other.cursor.removeSelectedText()
        self.lastAction(other)

@RegisterAction("normal")
class ChangeInnerWord(BaseInnerWord):
    def __init__(self):
        self.key = [Qt.Key_C, Qt.Key_I, Qt.Key_W]

    def lastAction(self, other):
        actions["EnterInsertMode"].performAction(other)

@RegisterAction("normal")
class DeleteInnerWord(BaseInnerWord):
    def __init__(self):
        self.key = [Qt.Key_D, Qt.Key_I, Qt.Key_W]

    def lastAction(self, other):
        other.cursor.removeSelectedText()