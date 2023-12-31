from lineedit import MyLineEdit
from constructors import Parenthesis
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
        scene.clipboard.serializeSelected()
        scene.deleteSelection()
        scene.clearSelection()
        scene.enterInsertMode()


@RegisterAction("visual")
class DeleteInVisual:
    def __init__(self):
        self.key = [Qt.Key_D]


    def performAction(self, other):
        scene.clipboard.serializeSelected()
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
        scene.history.store("remove line")


@RegisterAction("visual")
class Yank:
    def __init__(self):
        self.key = [Qt.Key_Y]

        
    def performAction(self, other):
        scene.clipboard.serializeSelected()
        scene.enterNormalMode()


@RegisterAction("normal")
class Paste:
    def __init__(self):
        self.key = [Qt.Key_P]

        
    def performAction(self, other):
        scene.clipboard.deserializeFromClipboard()
        scene.history.store("deserializing from clipboard")


@RegisterAction("normal")
class Undo:
    def __init__(self):
        self.key = [Qt.Key_U]

        
    def performAction(self, other):
        scene.history.undo()


@RegisterAction("normal")
class Redo:
    def __init__(self):
        self.key = [Qt.ControlModifier | Qt.Key_R]

        
    def performAction(self, other):
        scene.history.redo()

        
class InsideParenthesis:
    def __init__(self):
        self.key = [
            [Qt.Key_I, Qt.ShiftModifier | Qt.Key_ParenLeft],
            [Qt.Key_I, Qt.ShiftModifier | Qt.Key_ParenRight],
            ]


    def performAction(self, other):
        currentElement = other.parent
        while not isinstance(currentElement, Parenthesis):
            if currentElement == scene.frames[0]:
                return
            currentElement = currentElement.parent
        # we found that we where inside a parenthesis, let's select its contents
        scene.selectionFirst = [currentElement.base.children[0], 0]
        currentElement.base.children[-1].setFocus()
        currentElement.base.children[-1].setCursorPosition(len(currentElement.base.children[-1].text()))

        self.lastAction()


@RegisterAction("normal")
class DeleteInsideParenthesis(InsideParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_D)
    
    
    def lastAction(self):
        scene.updateVisualSelection()
        scene.clipboard.serializeSelected()
        scene.deleteSelection(selection=None, storeHistory=False)
        scene.clearSelection()
        scene.history.store("removed inside parenthesis")


@RegisterAction("normal")
class ChangeInsideParenthesis(InsideParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_C)
    
    
    def lastAction(self):
        scene.updateVisualSelection()
        scene.clipboard.serializeSelected()
        scene.deleteSelection(selection=None, storeHistory=False)
        scene.clearSelection()
        scene.history.store("removed inside parenthesis")
        scene.enterInsertMode()


@RegisterAction("visual")
class VisualInsideParenthesis(InsideParenthesis):
    def __init__(self):
        super().__init__()
    
    
    def lastAction(self):
        pass


class AroundParenthesis:
    def __init__(self):
        self.key = [
            [Qt.Key_A, Qt.ShiftModifier | Qt.Key_ParenLeft],
            [Qt.Key_A, Qt.ShiftModifier | Qt.Key_ParenRight],
            ]


    def performAction(self, other):
        currentElement = other.parent
        while not isinstance(currentElement, Parenthesis):
            if currentElement == scene.frames[0]:
                return
            currentElement = currentElement.parent
        # we found that we where inside a parenthesis, let's select it
        scene.selectionFirst = [currentElement.base.children[0], 0]
        currentElement.base.children[-1].nextLinedit.setFocus()
        currentElement.base.children[-1].nextLinedit.setCursorPosition(0)

        self.lastAction()


@RegisterAction("normal")
class DeleteAroundParenthesis(AroundParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_D)
    
    
    def lastAction(self):
        scene.updateVisualSelection()
        scene.clipboard.serializeSelected()
        scene.deleteSelection(selection=None, storeHistory=False)
        scene.clearSelection()
        scene.history.store("removed around parenthesis")


@RegisterAction("normal")
class ChangeAroundParenthesis(AroundParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_C)
    
    
    def lastAction(self):
        scene.updateVisualSelection()
        scene.clipboard.serializeSelected()
        scene.deleteSelection(selection=None, storeHistory=False)
        scene.clearSelection()
        scene.history.store("removed around parenthesis")
        scene.enterInsertMode()


@RegisterAction("visual")
class VisualAroundParenthesis(AroundParenthesis):
    def __init__(self):
        super().__init__()
    
    
    def lastAction(self):
        pass


@RegisterAction("normal")
class DeleteSurroundingParenthesis(AroundParenthesis):
    def __init__(self):
        self.key = [
            [Qt.Key_D, Qt.Key_S, Qt.ShiftModifier | Qt.Key_ParenLeft],
            [Qt.Key_D, Qt.Key_S, Qt.ShiftModifier | Qt.Key_ParenRight],
            ]


    def performAction(self, other):
        currentElement = other.parent
        while not isinstance(currentElement, Parenthesis):
            if currentElement == scene.frames[0]:
                return
            currentElement = currentElement.parent
        # we found that we where inside a parenthesis, let's select it
        selection = []
        register = []
        selection.append((currentElement.base.children[0], 0))
        for element in currentElement.base.children[1:-1]:
            selection.append((element, None))
        selection.append((currentElement.base.children[-1], len(currentElement.base.children[-1].text())))
        scene.clipboard.serializeSelected(selection=selection, register=register)
        currentElement.removeFrame()
        scene.clipboard.deserializeFromClipboard(register)
        scene.history.store("removed surrounding parenthesis")
