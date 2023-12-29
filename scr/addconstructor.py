from base import RegisterAction
from constructors import Fraction, Parenthesis, SquareRoot, Subscript, Superscript, SuperSubscript
from constructors import subscript
from constructors import supersubscript
from constructors import superscript
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


@RegisterAction("normal")
class CreateSuperscript:
    def __init__(self):
        self.key = [Qt.Key_2]

        
    def performAction(self, other):
        # look for the frame to the left
        indx = other.parent.children.index(other)
        cursorPosition = other.cursorPosition()
        if cursorPosition == 0:
            if indx == 0:
                return
            # check what we have to the left
            leftElement = other.parent.children[indx-1]
            if isinstance(leftElement, Superscript): 
                return
            if isinstance(leftElement, SuperSubscript): 
                return
            if isinstance(leftElement, Subscript): 
                leftElement.__class__ = SuperSubscript
                leftElement.base.__class__ = supersubscript.Base
                leftElement.superscript = supersubscript.Superior(leftElement)
                leftElement.superscript.setFirstLineEdit()
                leftElement.children.append(leftElement.superscript)
                leftElement.subscript.__class__ = supersubscript.Inferior
                scene.updateFrames()
                return
            selection = [(leftElement, None)]
            register = []
            scene.clipboard.serializeSelected(selection, register)
            newFrame = other.createFrameMiddle(Superscript)
            leftElement.removeFrame()
            newFrame.base.firstLinedit.setFocus()
            scene.clipboard.deserializeFromClipboard(register)
            return
                
        # check if we are at the end of the base of a script
        if cursorPosition == len(other.text()):
            if isinstance(other.parent, subscript.Base):
                element = other.parent.parent
                element.__class__ = SuperSubscript
                element.base.__class__ = supersubscript.Base
                element.superscript = supersubscript.Superior(element)
                element.superscript.setFirstLineEdit()
                element.children.append(element.superscript)
                element.subscript.__class__ = supersubscript.Inferior
                scene.updateFrames()
                return
            if isinstance(other.parent, supersubscript.Base):
                return
            if isinstance(other.parent, superscript.Base):
                return

        # we are in the middle of a lineEdit
        newFrame = other.createFrameMiddle(Superscript)
        characterLeft = other.text()[-1]
        newFrame.base.firstLinedit.setText(characterLeft)
        other.setText(other.text()[:-1])


@RegisterAction("normal")
class CreateJustSuperscriptDebug:
    def __init__(self):
        self.key = [Qt.Key_3]

        
    def performAction(self, other):
        other.createFrameMiddle(Superscript)


@RegisterAction("normal")
class CreateJustSuperscriptDebug:
    def __init__(self):
        self.key = [Qt.Key_4]

        
    def performAction(self, other):
        other.createFrameMiddle(SuperSubscript)


        
@RegisterAction("normal")
class CreateParenthesis:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_ParenLeft]

        
    def performAction(self, other):
        other.createFrameMiddle(Parenthesis)
