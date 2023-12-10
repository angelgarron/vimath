from PySide6.QtCore import Qt
from scene import scene

actions = {}
actionsVisual = {}
actionsInsert = {}
def RegisterAction(whichMode="normal"):
    def wrapper(f):
        if whichMode == "normal":
            actions.update({f.__name__:f()})
        elif whichMode == "visual": 
            actionsVisual.update({f.__name__:f()})
        elif whichMode == "both":
            actions.update({f.__name__:f()})
            actionsVisual.update({f.__name__:f()})
        elif whichMode == "insert":
            actionsInsert.update({f.__name__:f()})
    return wrapper


@RegisterAction("normal")
class EnterInsertMode:
    def __init__(self):
        self.key = [Qt.Key_I]


    def performAction(self, other):
        scene.enterInsertMode()


@RegisterAction("normal")
class EnterInsertModeAppend:
    def __init__(self):
        self.key = [Qt.Key_A]


    def performAction(self, other):
        other.cursorForward(False)
        scene.enterInsertMode()


@RegisterAction("both")
class ToggleVisualMode:
    def __init__(self):
        self.key = [Qt.Key_V]


    def performAction(self, other):
        if scene.isNormalMode():
            scene.selectionFirst = [other, other.cursorPosition()]
            scene.enterVisualMode()
        else:
            scene.selectionFirst = None
            scene.selectionSecond = None
            scene.enterNormalMode()
        scene.printSelection()
