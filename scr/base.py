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
    def performAction(self, other, moveAnchor="default"):
        if other.mode == 2:
            mark = True
        else:
            mark = False
        
        if moveAnchor == True:
            mark = False
        elif moveAnchor == False:
            mark = True

        if isinstance(self.movement, list):
            for m in self.movement:
                m(other, mark)
        else:
            self.movement(other, mark)


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
        actions["MoveRight"].performAction(other)
        other.enterInsertMode()


@RegisterAction("normal")
class EnterVisualMode:
    def __init__(self):
        self.key = [Qt.Key_V]


    def performAction(self, other):
        other.enterVisualMode()
