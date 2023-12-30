from PySide6.QtCore import Qt
from scene import scene

actions = {}
actionsVisual = {}
actionsInsert = {}
def RegisterAction(whichMode="normal"):
    def decorator(constructor):
        if whichMode == "normal":
            actions.update({constructor.__name__:constructor()})
        elif whichMode == "visual": 
            actionsVisual.update({constructor.__name__:constructor()})
        elif whichMode == "both":
            actions.update({constructor.__name__:constructor()})
            actionsVisual.update({constructor.__name__:constructor()})
        elif whichMode == "insert":
            actionsInsert.update({constructor.__name__:constructor()})
        return constructor
    return decorator


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
            scene.enterVisualMode()
        else:
            scene.enterNormalMode()


@RegisterAction("normal")
class Load:
    def __init__(self):
        self.key = [Qt.ControlModifier | Qt.Key_L]


    def performAction(self, other):
        scene.loadFromFile("saved_scene.json")


@RegisterAction("normal")
class Save:
    def __init__(self):
        self.key = [Qt.ControlModifier | Qt.Key_S]


    def performAction(self, other):
        scene.saveToFile("saved_scene.json")
