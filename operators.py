from base import RegisterAction, BaseMovement, KeyCombination, actions
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import Qt

class BaseInnerWord:
    def __init__(self):
        self.key = [Qt.Key_I, Qt.Key_W]

    def performAction(self, other):
        actions["MoveBeginningWord"].performAction(other)
        actions["MoveWordEnd"].performAction(other, moveAnchor=False)
        self.lastAction(other)

@RegisterAction("normal")
class ChangeInnerWord(BaseInnerWord):
    def __init__(self):
        super().__init__()
        self.key.insert(0, Qt.Key_C)

    def lastAction(self, other):
        other.cursor.removeSelectedText()
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

def findClosingParenthesis(s, cursorPosition):
    closingParenthesisPosition = 0
    for char in s[cursorPosition:]:
        if char == "(":
            closingParenthesisPosition = -1
            return closingParenthesisPosition
        elif char == ")":
            closingParenthesisPosition = cursorPosition + closingParenthesisPosition
            return closingParenthesisPosition
        closingParenthesisPosition += 1
    closingParenthesisPosition = -1
    return closingParenthesisPosition

def findOpeningParenthesis(s, cursorPosition):
    openingParenthesisPosition = 0
    for c in reversed(s[:cursorPosition+1]):
        openingParenthesisPosition += 1
        if c == "(":
            openingParenthesisPosition = cursorPosition + 1 - openingParenthesisPosition
            return openingParenthesisPosition
        elif c == ")":
            openingParenthesisPosition = -1
            return openingParenthesisPosition
    openingParenthesisPosition = -1
    return openingParenthesisPosition

def findOtherClosingParenthesis(s, cursorPosition):
    parenthesisCounter = 1
    closingParenthesisPosition = 0
    for c in s[cursorPosition+1:]:
        if c == "(":
            parenthesisCounter += 1
        elif c == ")":
            parenthesisCounter -= 1
        if parenthesisCounter == 0:
            closingParenthesisPosition = closingParenthesisPosition + cursorPosition + 1
            return closingParenthesisPosition
        closingParenthesisPosition += 1
    closingParenthesisPosition = -1
    return closingParenthesisPosition

def findOtherOpeningParenthesis(s, cursorPosition):
    parenthesisCounter = 1
    openingParenthesisPosition = 0
    for c in reversed(s[:cursorPosition]):
        openingParenthesisPosition += 1
        if c == "(":
            parenthesisCounter -= 1
        elif c == ")":
            parenthesisCounter += 1
        if parenthesisCounter == 0:
            openingParenthesisPosition = cursorPosition - openingParenthesisPosition
            return openingParenthesisPosition
    openingParenthesisPosition = -1
    return openingParenthesisPosition

def findOtherParenthesis(s, openingParenthesisPosition, closingParenthesisPosition, cursorPosition):
    if openingParenthesisPosition == -1:
        openingParenthesisPosition = findOtherOpeningParenthesis(s, cursorPosition)
    else:
        closingParenthesisPosition = findOtherClosingParenthesis(s, cursorPosition)
    return openingParenthesisPosition, closingParenthesisPosition

class BaseInnerParenthesis:
    def __init__(self):
        self.key = [[Qt.Key_I, KeyCombination(Qt.ShiftModifier, Qt.Key_ParenRight)], 
                    [Qt.Key_I, KeyCombination(Qt.ShiftModifier, Qt.Key_ParenLeft)]]

    def performAction(self, other):
        plainText = other.toPlainText()
        cursorPosition = other.cursor.position()

        openingParenthesisPosition = findOpeningParenthesis(plainText, cursorPosition)
        closingParenthesisPosition = findClosingParenthesis(plainText, cursorPosition)

        if not (closingParenthesisPosition == -1 and openingParenthesisPosition == -1):
            openingParenthesisPosition, closingParenthesisPosition = findOtherParenthesis(plainText,
                                                                                          openingParenthesisPosition, 
                                                                                          closingParenthesisPosition, 
                                                                                          cursorPosition)

            other.cursor.setPosition(openingParenthesisPosition+1, other.cursor.MoveMode.MoveAnchor)
            other.cursor.setPosition(closingParenthesisPosition, other.cursor.MoveMode.KeepAnchor)
            self.lastAction(other)

@RegisterAction("normal")
class ChangeInsideParenthesis(BaseInnerParenthesis):
    def __init__(self):
        super().__init__()
        for key in self.key:
            key.insert(0, Qt.Key_C)

    def lastAction(self, other):
        other.cursor.removeSelectedText()
        actions["EnterInsertMode"].performAction(other)

@RegisterAction("normal")
class DeleteInsideParenthesis(BaseInnerParenthesis):
    def __init__(self):
        super().__init__()
        for key in self.key:
            key.insert(0, Qt.Key_D)

    def lastAction(self, other):
        other.cursor.removeSelectedText()
