from base import RegisterAction
from constructors import Fraction, Parenthesis, SquareRoot, Subscript, Superscript, SuperSubscript
from PySide6.QtGui import Qt
from scene import scene


@RegisterAction("normal")
class CreateFraction:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_F]

        
    def performAction(self, other):
        other.createFrameMiddle(Fraction)


@RegisterAction("normal")
class CreateSquareRoot:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_S]

        
    def performAction(self, other):
        other.createFrameMiddle(SquareRoot)


@RegisterAction("normal")
class CreateIntegral:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_I]

        
    def performAction(self, other):
        cursorPosition = other.cursorPosition()
        text = other.text()
        text = list(text)
        text.insert(cursorPosition, "∫")
        text = "".join(text)
        other.setText(text)
        other.setCursorPosition(cursorPosition+1)


@RegisterAction("normal")
class CreateSubscript:
    def __init__(self):
        self.key = [Qt.Key_1]

        
    def performAction(self, other):
        newFrame = other.createFrameMiddle(Subscript)

        if len(other.text()) == 0:
            # look for the frame to the left
            indx = other.parent.children.index(other)
            if indx == 0: # there is nothing to the left
                return
            leftElement = other.parent.children[indx-1]
            selection = [(leftElement, None)]
            register = []
            scene.clipboard.serializeSelected(selection, register)
            leftElement.removeFrame()
            newFrame.base.firstLinedit.setFocus()
            scene.clipboard.deserializeFromClipboard(register)
            return

        # if we are in the middle of a lineEdit, just take the character to the left
        characterLeft = other.text()[-1]
        if characterLeft:
            newFrame.base.firstLinedit.setText(characterLeft)
            other.setText(other.text()[:-1])
            return


@RegisterAction("insert")
class CreateSuperscript:
    def __init__(self):
        self.key = ["^"]

        
    def performAction(self, other, cursorPosition, text):
        # need to transform to a list in order to use pop
        text = list(text)
        text.pop(cursorPosition)
        character = text.pop(cursorPosition-1)
        other.setText("".join(text))
        other.setCursorPosition(cursorPosition-1)
        newFrame = other.createFrameMiddle(Superscript)
        newFrame.baseCharacter.children[0].setText(character)
        newFrame.superscript.children[0].setFocus()
        newFrame.scene.enterInsertMode()

        
@RegisterAction("normal")
class CreateParenthesis:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_ParenLeft]

        
    def performAction(self, other):
        other.createFrameMiddle(Parenthesis)
