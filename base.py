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
def RegisterAction(f):
    actions.update({f.__name__:f()})
    return None

class BaseMovement:
    def performAction(self, other):
        if isinstance(self.movement, list):
            for m in self.movement:
                other.cursor.movePosition(m, other.cursor.MoveMode.MoveAnchor, 1)
        else:
            other.cursor.movePosition(self.movement, other.cursor.MoveMode.MoveAnchor, 1)
        other.setTextCursor(other.cursor)

@RegisterAction
class EnterInsertMode:
    def __init__(self):
        self.key = [Qt.Key_I]

    def performAction(self, other):
        other.enterInsertMode()
        other.storedKeys = []