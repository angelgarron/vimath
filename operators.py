from base import RegisterAction, BaseMovement, KeyCombination, actions
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import Qt

class BaseInnerWord:
    def __init__(self):
        self.key = [Qt.Key_I, Qt.Key_W]

    def performAction(self, other):
        actions["MoveBeginningWord"].performAction(other)
        actions["MoveWordEnd"].performAction(other, moveAnchor=False)
        other.cursor.removeSelectedText()
        self.lastAction(other)

@RegisterAction("normal")
class ChangeInnerWord(BaseInnerWord):
    def __init__(self):
        super().__init__()
        self.key.insert(0, Qt.Key_C)

    def lastAction(self, other):
        actions["EnterInsertMode"].performAction(other)

@RegisterAction("normal")
class DeleteInnerWord(BaseInnerWord):
    def __init__(self):
        super().__init__()
        self.key.insert(0, Qt.Key_D)

    def lastAction(self, other):
        other.cursor.removeSelectedText()

@RegisterAction("visual")
class ChangeInVisual:
    def __init__(self):
        self.key = [Qt.Key_C]

    def performAction(self, other):
        other.cursor.removeSelectedText()
        actions["EnterInsertMode"].performAction(other)

@RegisterAction("visual")
class DeleteInVisual:
    def __init__(self):
        self.key = [Qt.Key_D]

    def performAction(self, other):
        other.cursor.removeSelectedText()
        other.enterNormalMode()

@RegisterAction("normal")
class InsertBeginningLine:
    def __init__(self):
        self.key = [KeyCombination(Qt.ShiftModifier, Qt.Key_I)]

    def performAction(self, other):
        actions["MoveStartOfLine"].performAction(other)
        actions["EnterInsertMode"].performAction(other)

@RegisterAction("normal")
class InsertEndLine:
    def __init__(self):
        self.key = [KeyCombination(Qt.ShiftModifier, Qt.Key_A)]

    def performAction(self, other):
        actions["MoveEndOfLine"].performAction(other)
        actions["EnterInsertMode"].performAction(other)
