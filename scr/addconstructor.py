from base import RegisterAction
from matheditor import MyFrame, Fraction, SquareRoot, Subscript, Superscript
from PySide6.QtGui import Qt


@RegisterAction("normal")
class CreateFraction:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_F]

        
    def performAction(self, other):
        newFrame = other.parent.createFrameMiddle(other, Fraction)
        newFrame.show()
        MyFrame.updateFrames()


@RegisterAction("normal")
class CreateSquareRoot:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_S]

        
    def performAction(self, other):
        newFrame = other.parent.createFrameMiddle(other, SquareRoot)
        newFrame.show()
        MyFrame.updateFrames()


@RegisterAction("insert")
class CreateSubscript:
    def __init__(self):
        self.key = ["_"]

        
    def performAction(self, other, cursorPosition, text):
        # need to transform to a list in order to use pop
        text = list(text)
        text.pop(cursorPosition)
        character = text.pop(cursorPosition-1)
        other.setText("".join(text))
        other.setCursorPosition(cursorPosition-1)
        newFrame = other.parent.createFrameMiddle(other, Subscript)
        newFrame.baseCharacter.children[0].setText(character)
        newFrame.subscript.children[0].setFocus()
        newFrame.show()
        MyFrame.updateFrames()


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
        newFrame = other.parent.createFrameMiddle(other, Superscript)
        newFrame.baseCharacter.children[0].setText(character)
        newFrame.superscript.children[0].setFocus()
        newFrame.show()
        MyFrame.updateFrames()
