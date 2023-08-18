from PySide6.QtCore import Qt

class KeyCombination:
    def __init__(self, modifier, key):
        self.modifier = modifier
        self.key = key
    def __eq__(self, other):
        if not isinstance(other, KeyCombination):
            return False
        return self.key == other.key and self.modifier == other.modifier

actions = {}
actionsVisual = {}
def RegisterAction(whichMode="normal"):
    def wrapper(f):
        if whichMode == "normal":
            actions.update({f.__name__:f()})
        elif whichMode == "visual": 
            actionsVisual.update({f.__name__:f()})
        elif whichMode == "both":
            actions.update({f.__name__:f()})
            actionsVisual.update({f.__name__:f()})
    return wrapper

class BaseMovement:
    def performAction(self, other, moveAnchor=True):
        if other.mode == 2 or not moveAnchor:
            moveMode = other.cursor.MoveMode.KeepAnchor
        else:
            moveMode = other.cursor.MoveMode.MoveAnchor

        if isinstance(self.movement, list):
            for m in self.movement:
                other.cursor.movePosition(m, moveMode, 1)
        else:
            other.cursor.movePosition(self.movement, moveMode, 1)
        other.setTextCursor(other.cursor)

@RegisterAction("normal")
class EnterInsertMode:
    def __init__(self):
        self.key = [Qt.Key_I]

    def performAction(self, other):
        other.enterInsertMode()

@RegisterAction("normal")
class EnterVisualMode:
    def __init__(self):
        self.key = [Qt.Key_V]

    def performAction(self, other):
        other.enterVisualMode()
