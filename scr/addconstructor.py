from base import RegisterAction
from matheditor import MyFrame, Fraction, SquareRoot, Subscript
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


@RegisterAction("normal")
# FIXME do in insert mode
class CreateSubscript:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_Underscore]

        
    def performAction(self, other):
        # need to transform to a list in order to use pop
        text = list(other.text())
        character = text.pop(other.cursorPosition()-1)
        text = "".join(text)
        cursorPosition = other.cursorPosition()
        other.setText(text)
        other.setCursorPosition(cursorPosition-1)
        newFrame = other.parent.createFrameMiddle(other, Subscript)
        newFrame.baseCharacter.children[0].setText(character)
        newFrame.subscript.children[0].setFocus()
        newFrame.show()
        MyFrame.updateFrames()
