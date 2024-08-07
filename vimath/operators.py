from vimath.lineedit import MyLineEdit
from vimath import constructors
from vimath.constructors import Parenthesis, mainframe
from vimath.base import RegisterAction
from vimath.scene import scene
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
        previousLineEdit = other
        while previousLineEdit.previousLineEdit:
            previousLineEdit = previousLineEdit.previousLineEdit
        previousLineEdit.home(False)
        previousLineEdit.setFocus()
        scene.enterInsertMode()


@RegisterAction("normal")
class InsertEndLine:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_A]


    def performAction(self, other):
        nextLineEdit = other
        while nextLineEdit.nextLineEdit:
            nextLineEdit = nextLineEdit.nextLineEdit
        nextLineEdit.end(False)
        nextLineEdit.setFocus()
        scene.enterInsertMode()


@RegisterAction("insert")
class RemoveFrame:
    def __init__(self):
        self.key = [Qt.Key_Backspace]

        
    def performAction(self, other):
        if other.cursorPosition() == 0:
            if len(other.parent.children) == 1:
                if isinstance(other.parent, (
                    constructors.superscript.Superior,
                    constructors.subscript.Inferior,
                    constructors.supersubscript.Superior,
                    constructors.supersubscript.Inferior,
                    )):
                    other.parent.parent.base.lastLineEdit.setFocus()
                    return
                other = other.parent.parent.removeFrame()
                return
            else: # see what we have to the left
                indx = other.parent.children.index(other)
                leftElement = other.parent.children[indx-1]
                leftElement.removeFrame()
        other.backspace()


@RegisterAction("normal")
class RemoveLine:
    def __init__(self):
        self.key = [Qt.Key_D, Qt.Key_D]

        
    def performAction(self, other):
        # find the Line where we are
        currentLine = other
        while not isinstance(currentLine, mainframe.Line):
            currentLine = currentLine.parent
        selection = []
        selection.append((currentLine, None))
        scene.clipboard.serializeSelected(selection=selection)
        currentLine.removeLine()
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
class PasteUp:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_P]

        
    def performAction(self, other):
        scene.clipboard.deserializeFromClipboard(up=True)
        scene.history.store("deserializing from clipboard up")


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
            if currentElement == scene.window.mainMathFrame:
                return
            currentElement = currentElement.parent
        # we found that we where inside a parenthesis, let's select its contents
        scene.selectionFirst = [currentElement.base.firstLineEdit, 0]
        currentElement.base.lastLineEdit.setFocus()
        currentElement.base.lastLineEdit.end(False)


@RegisterAction("normal")
class DeleteInsideParenthesis(InsideParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_D)
    
    
    def performAction(self, other):
        super().performAction(other)
        scene.updateVisualSelection()
        scene.clipboard.serializeSelected()
        scene.deleteSelection(selection=None, storeHistory=False)
        scene.clearSelection()
        scene.history.store("removed inside parenthesis")


class UntilEnd:
    def performAction(self, other):
        # go until the end of the line
        lastLineEdit = other
        while lastLineEdit.nextLineEdit:
            lastLineEdit = lastLineEdit.nextLineEdit

        scene.selectionFirst = [other, other.cursorPosition()]
        lastLineEdit.setFocus()
        lastLineEdit.end(False)
        scene.updateVisualSelection()
        scene.clipboard.serializeSelected()
        scene.deleteSelection(selection=None, storeHistory=False)
        scene.clearSelection()
        scene.history.store("removed until end of line")


@RegisterAction("normal")
class DeleteUntilEnd(UntilEnd):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_D]


@RegisterAction("normal")
class ChangeUntilEnd(UntilEnd):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_C]
    

    def performAction(self, other):
        super().performAction(other)
        scene.enterInsertMode()
    

@RegisterAction("normal")
class ChangeInsideParenthesis(InsideParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_C)
    
    
    def performAction(self, other):
        super().performAction(other)
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
    
    
@RegisterAction("normal")
class YankInsideParenthesis(InsideParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_Y)
    
    
    def performAction(self, other):
        super().performAction(other)
        scene.updateVisualSelection()
        scene.clipboard.serializeSelected()
        scene.clearSelection()


class AroundParenthesis:
    def __init__(self):
        self.key = [
            [Qt.Key_A, Qt.ShiftModifier | Qt.Key_ParenLeft],
            [Qt.Key_A, Qt.ShiftModifier | Qt.Key_ParenRight],
            ]


    def performAction(self, other):
        currentElement = other.parent
        while not isinstance(currentElement, Parenthesis):
            if currentElement == scene.window.mainMathFrame:
                return
            currentElement = currentElement.parent
        # we found that we where inside a parenthesis, let's select it
        scene.selectionFirst = [currentElement.base.firstLineEdit, 0]
        currentElement.base.lastLineEdit.nextLineEdit.setFocus()
        currentElement.base.lastLineEdit.nextLineEdit.home(False)


@RegisterAction("normal")
class DeleteAroundParenthesis(AroundParenthesis):
    def __init__(self):
        super().__init__()
        for combination in self.key:
            combination.insert(0, Qt.Key_D)
    
    
    def performAction(self, other):
        super().performAction(other)
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
    
    
    def performAction(self, other):
        super().performAction(other)
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
    
    
@RegisterAction("normal")
class DeleteSurroundingParenthesis:
    def __init__(self):
        self.key = [
            [Qt.Key_D, Qt.Key_S, Qt.ShiftModifier | Qt.Key_ParenLeft],
            [Qt.Key_D, Qt.Key_S, Qt.ShiftModifier | Qt.Key_ParenRight],
            ]


    def performAction(self, other):
        currentElement = other.parent
        while not isinstance(currentElement, Parenthesis):
            if currentElement == scene.window.mainMathFrame:
                return
            currentElement = currentElement.parent
        # we found that we where inside a parenthesis, let's select it
        selection = []
        register = []
        selection.append((currentElement.base.firstLineEdit, 0))
        for element in currentElement.base.children[1:-1]:
            selection.append((element, None))
        selection.append((currentElement.base.lastLineEdit, len(currentElement.base.lastLineEdit.text())))
        scene.clipboard.serializeSelected(selection=selection, register=register)
        currentElement.removeFrame()
        scene.clipboard.deserializeFromClipboard(register, up=True)
        scene.history.store("removed surrounding parenthesis")


@RegisterAction("normal")
class YankLine:
    def __init__(self):
        self.key = [Qt.Key_Y, Qt.Key_Y]

        
    def performAction(self, other):
        # find the Line where we are
        currentLine = other
        while not isinstance(currentLine, mainframe.Line):
            currentLine = currentLine.parent
        selection = []
        selection.append((currentLine, None))
        scene.clipboard.serializeSelected(selection=selection)
