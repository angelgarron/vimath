from base import RegisterAction
from scene import scene
from PySide6.QtGui import Qt

class BaseInnerWord:
    def __init__(self):
        self.key = [Qt.Key_I, Qt.Key_W]


    def performAction(self, other):
        other.cursorWordBackward(True)
        movements = [
                    other.cursorWordForward, 
                    other.cursorWordForward, 
                    other.cursorBackward, 
                    other.cursorBackward, 
                    ]

        for movement in movements:
            movement(False)
        

        self.lastAction(other)


@RegisterAction("normal")
class ChangeInnerWord(BaseInnerWord):
    def __init__(self):
        super().__init__()
        self.key.insert(0, Qt.Key_C)


    def lastAction(self, other):
        other.del_()
        scene.enterInsertMode()


@RegisterAction("normal")
class DeleteInnerWord(BaseInnerWord):
    def __init__(self):
        super().__init__()
        self.key.insert(0, Qt.Key_D)


    def lastAction(self, other):
        other.del_()


@RegisterAction("visual")
class VisualInnerWord(BaseInnerWord):
    def lastAction(self, other):
        pass


@RegisterAction("visual")
class ChangeInVisual:
    def __init__(self):
        self.key = [Qt.Key_C]


    def performAction(self, other):
        scene.deleteSelection()
        scene.clearSelection()
        scene.enterInsertMode()


@RegisterAction("visual")
class DeleteInVisual:
    def __init__(self):
        self.key = [Qt.Key_D]


    def performAction(self, other):
        scene.deleteSelection()
        scene.enterNormalMode()


@RegisterAction("normal")
class InsertBeginningLine:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_I]


    def performAction(self, other):
        previousLinedit = other
        while previousLinedit.previousLinedit:
            previousLinedit = previousLinedit.previousLinedit
        previousLinedit.home(False)
        previousLinedit.setFocus()
        scene.enterInsertMode()


@RegisterAction("normal")
class InsertEndLine:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_A]


    def performAction(self, other):
        nextLinedit = other
        while nextLinedit.nextLinedit:
            nextLinedit = nextLinedit.nextLinedit
        nextLinedit.end(False)
        nextLinedit.setFocus()
        scene.enterInsertMode()


@RegisterAction("normal")
class RemoveFrame:
    def __init__(self):
        self.key = [Qt.Key_Backspace]

        
    def performAction(self, other):
        if not other.text():
            other = other.parent.parent.removeFrame()


@RegisterAction("normal")
class RemoveLine:
    def __init__(self):
        self.key = [Qt.Key_D, Qt.Key_D]

        
    def performAction(self, other):
        scene.clear()


@RegisterAction("visual")
class Cut:
    def __init__(self):
        self.key = [Qt.ControlModifier | Qt.Key_X]

        
    def performAction(self, other):
        print("cutting")
        scene.clipboard.serializeSelected()
        scene.enterNormalMode()


@RegisterAction("normal")
class Paste:
    def __init__(self):
        self.key = [Qt.ControlModifier | Qt.Key_V]

        
    def performAction(self, other):
        print("pasting")
        scene.clipboard.deserializeFromClipboard()
