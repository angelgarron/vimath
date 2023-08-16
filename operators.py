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

@RegisterAction("normal")
class InsertEndLine:
    def __init__(self):
        self.key = [Qt.Key_A]

    def performAction(self, other):
        plainText = other.toPlainText()
        cursorPosition = other.cursor.position()

        openBracketPosition = 0
        closeBracketPosition = 0
        for i, c in enumerate(plainText[cursorPosition:]):
            if c == "(":
                closeBracketPosition = -1
                break
            elif c == ")":
                closeBracketPosition = cursorPosition+closeBracketPosition
                break
            closeBracketPosition += 1

        for i, c in reversed(list(enumerate(plainText[:cursorPosition]))):
            openBracketPosition += 1
            if c == "(":
                break
            elif c == ")":
                openBracketPosition = -1
                break
        closeBracketPosition_other = -1
        openBracketPosition_other = -1
        if openBracketPosition != -1:
            openBracketPosition = cursorPosition-openBracketPosition
            counter = 1
            for i, c in enumerate(plainText[cursorPosition:]):
                if c == "(":
                    counter += 1
                elif c == ")":
                    counter -= 1
                if counter == 0:
                    closeBracketPosition_other = i+cursorPosition
                    break
        else:
            counter = 1
            for i, c in reversed(list(enumerate(plainText[:cursorPosition]))):
                if c == "(":
                    counter -= 1
                elif c == ")":
                    counter += 1
                if counter == 0:
                    openBracketPosition_other = i
                    break
        print(plainText, cursorPosition, openBracketPosition, closeBracketPosition, 
              openBracketPosition_other, closeBracketPosition_other)
