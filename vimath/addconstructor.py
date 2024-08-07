from vimath.base import RegisterAction
from vimath.constructors import (Fraction, Parenthesis, SquareRoot, Subscript, Superscript, SuperSubscript,
                                 subscript, supersubscript, superscript, mainframe)
from PySide6.QtGui import Qt
from vimath.scene import scene


def visualSurround(originalConstructor):
    def performAction(self, other):
        register = []
        scene.clipboard.serializeSelected(scene.selection, register)
        scene.deleteSelection(storeHistory=False)
        scene.getLineEditWithFocus().createFrameMiddle(self.constructor, storeHistory=False)
        scene.clipboard.deserializeFromClipboard(register)
        scene.enterNormalMode()
        scene.history.store(f"surrounded version of {originalConstructor.__name__}")

    newConstructor = type(
        f"Surround{originalConstructor.__name__}",
        (originalConstructor, ),
        {
            "performAction": performAction
        }
    )
    RegisterAction("visual")(newConstructor)
    return newConstructor


class Constructor:
    def performAction(self, other):
        other.createFrameMiddle(self.constructor)


@visualSurround
@RegisterAction(["normal", "insert"])
class CreateFraction(Constructor):
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_F]
        self.constructor = Fraction

    
@visualSurround
@RegisterAction(["normal", "insert"])
class CreateSquareRoot(Constructor):
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_S]
        self.constructor = SquareRoot


@RegisterAction(["normal", "insert"])
class CreateIntegral:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_I]

        
    def performAction(self, other):
        cursorPosition = other.cursorPosition()
        text = other.text()
        text = list(text)
        text.insert(cursorPosition, chr(115))
        text = "".join(text)
        other.setText(text)
        other.setCursorPosition(cursorPosition+1)


@RegisterAction(["normal", "insert"])
class CreateSubscript:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Underscore]

        
    def performAction(self, other):
        # check if we are in a lineEdit in the base of a script
        element = other.parent.parent
        if isinstance(other.parent, superscript.Base):
            element.__class__ = SuperSubscript
            element.base.__class__ = supersubscript.Base
            element.subscript = supersubscript.Inferior(element)
            element.subscript.setFirstLineEdit()
            element.children.append(element.subscript)
            element.superscript.__class__ = supersubscript.Superior
            scene.updateFrames()
            element.subscript.firstLineEdit.setFocus()
            return
        if isinstance(other.parent, supersubscript.Base):
            element.subscript.firstLineEdit.setFocus()
            return
        if isinstance(other.parent, subscript.Base):
            element.subscript.firstLineEdit.setFocus()
            return

        # look for the frame to the left
        indx = other.parent.children.index(other)
        cursorPosition = other.cursorPosition()
        if cursorPosition == 0:
            if indx == 0:
                return
            # check what we have to the left
            leftElement = other.parent.children[indx-1]
            if isinstance(leftElement, Subscript): 
                leftElement.subscript.firstLineEdit.setFocus()
                return
            if isinstance(leftElement, SuperSubscript): 
                leftElement.subscript.firstLineEdit.setFocus()
                return
            if isinstance(leftElement, Superscript): 
                leftElement.__class__ = SuperSubscript
                leftElement.base.__class__ = supersubscript.Base
                leftElement.subscript = supersubscript.Inferior(leftElement)
                leftElement.subscript.setFirstLineEdit()
                leftElement.children.append(leftElement.subscript)
                leftElement.superscript.__class__ = supersubscript.Superior
                scene.updateFrames()
                leftElement.subscript.firstLineEdit.setFocus()
                return
            selection = [(leftElement, None)]
            register = []
            scene.clipboard.serializeSelected(selection, register)
            newFrame = other.createFrameMiddle(Subscript, storeHistory=False)
            leftElement.removeFrame()
            newFrame.base.firstLineEdit.setFocus()
            scene.clipboard.deserializeFromClipboard(register)
            newFrame.subscript.firstLineEdit.setFocus()
            return
                
        # we are in the middle of a lineEdit
        newFrame = other.createFrameMiddle(Subscript, storeHistory=False)
        characterLeft = other.text()[-1]
        newFrame.base.firstLineEdit.setText(characterLeft)
        other.setText(other.text()[:-1])
        newFrame.subscript.firstLineEdit.setFocus()


@RegisterAction("normal")
class CreateSuperscript:
    def __init__(self):
        self.key = [Qt.Key_2]

        
    def performAction(self, other):
        # check if we are in a lineEdit in the base of a script
        element = other.parent.parent
        if isinstance(other.parent, subscript.Base):
            element.__class__ = SuperSubscript
            element.base.__class__ = supersubscript.Base
            element.superscript = supersubscript.Superior(element)
            element.superscript.setFirstLineEdit()
            element.children.insert(0, element.superscript)
            element.subscript.__class__ = supersubscript.Inferior
            scene.updateFrames()
            element.superscript.firstLineEdit.setFocus()
            return
        if isinstance(other.parent, supersubscript.Base):
            element.superscript.firstLineEdit.setFocus()
            return
        if isinstance(other.parent, superscript.Base):
            element.superscript.firstLineEdit.setFocus()
            return

        # look for the frame to the left
        indx = other.parent.children.index(other)
        cursorPosition = other.cursorPosition()
        if cursorPosition == 0:
            if indx == 0:
                return
            # check what we have to the left
            leftElement = other.parent.children[indx-1]
            if isinstance(leftElement, Superscript): 
                leftElement.superscript.firstLineEdit.setFocus()
                return
            if isinstance(leftElement, SuperSubscript): 
                leftElement.superscript.firstLineEdit.setFocus()
                return
            if isinstance(leftElement, Subscript): 
                leftElement.__class__ = SuperSubscript
                leftElement.base.__class__ = supersubscript.Base
                leftElement.superscript = supersubscript.Superior(leftElement)
                leftElement.superscript.setFirstLineEdit()
                leftElement.children.insert(0, leftElement.superscript)
                leftElement.subscript.__class__ = supersubscript.Inferior
                scene.updateFrames()
                leftElement.superscript.firstLineEdit.setFocus()
                return
            selection = [(leftElement, None)]
            register = []
            scene.clipboard.serializeSelected(selection, register)
            newFrame = other.createFrameMiddle(Superscript, storeHistory=False)
            leftElement.removeFrame()
            newFrame.base.firstLineEdit.setFocus()
            scene.clipboard.deserializeFromClipboard(register)
            newFrame.superscript.firstLineEdit.setFocus()
            return
                
        # we are in the middle of a lineEdit
        newFrame = other.createFrameMiddle(Superscript, storeHistory=False)
        characterLeft = other.text()[-1]
        newFrame.base.firstLineEdit.setText(characterLeft)
        other.setText(other.text()[:-1])
        newFrame.superscript.firstLineEdit.setFocus()


@visualSurround
@RegisterAction(["normal", "insert"])
class CreateParenthesis(Constructor):
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_ParenLeft]
        self.constructor = Parenthesis


@RegisterAction("normal")
class InsertNewLine:
    def __init__(self):
        self.key = [Qt.Key_O]

        
    def performAction(self, other):
        # find the Line where we are
        currentLine = other
        while not isinstance(currentLine, mainframe.Line):
            currentLine = currentLine.parent
        newFrame = scene.window.mainMathFrame.createLine(currentLine.lineNumber+1)
        newFrame.firstLineEdit.setFocus()
        scene.enterInsertMode()


@RegisterAction("normal")
class InsertNewLineUp:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_O]

        
    def performAction(self, other):
        # find the Line where we are
        currentLine = other
        while not isinstance(currentLine, mainframe.Line):
            currentLine = currentLine.parent
        newFrame = scene.window.mainMathFrame.createLine(currentLine.lineNumber)
        newFrame.firstLineEdit.setFocus()
        scene.enterInsertMode()
