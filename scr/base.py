from PySide6.QtCore import Qt

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
    def checkmark(self, other):
        if other.mode == 2:
            mark = True
        else:
            mark = False

        return mark

                
@RegisterAction("normal")
class EnterInsertMode:
    def __init__(self):
        self.key = [Qt.Key_I]


    def performAction(self, other):
        other.enterInsertMode()


@RegisterAction("normal")
class EnterInsertModeAppend:
    def __init__(self):
        self.key = [Qt.Key_A]


    def performAction(self, other):
        other.cursorForward(self.checkmark(other))
        other.enterInsertMode()


@RegisterAction("normal")
class EnterVisualMode:
    def __init__(self):
        self.key = [Qt.Key_V]


    def performAction(self, other):
        other.enterVisualMode()
