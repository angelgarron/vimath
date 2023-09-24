from base import RegisterAction
from matheditor import MyFrame, Fraction, SquareRoot
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
