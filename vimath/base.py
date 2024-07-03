from PySide6.QtCore import Qt
from vimath.scene import scene

actions = {}
actionsVisual = {}
actionsInsert = {}
def RegisterAction(whichMode):
    def decorator(constructor):
        if type(whichMode) != list:
            modes = [whichMode]
        else:
            modes = whichMode
        for mode in modes:
            if mode == "normal":
                actions.update({constructor.__name__:constructor()})
            elif mode == "visual": 
                actionsVisual.update({constructor.__name__:constructor()})
            elif mode == "insert":
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


@RegisterAction(["normal", "visual"])
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
