class RegisterAction:
    actions = []
    def __init__(self, action):
        RegisterAction.actions.append(action())

class BaseMovement:
    def moveCursor(self, cursor):
        if isinstance(self.movement, list):
            for m in self.movement:
                cursor.movePosition(m, cursor.MoveMode.MoveAnchor, 1)
        else:
            cursor.movePosition(self.movement, cursor.MoveMode.MoveAnchor, 1)