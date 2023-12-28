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
class CreateSuperscriptDebug:
    def __init__(self):
        self.key = [Qt.Key_2]

        
    def performAction(self, other):
        # look for the frame to the left
        indx = other.parent.children.index(other)
        cursorPosition = other.cursorPosition()
        if cursorPosition == 0:
            if indx == 0:
                print("there is nothing to the left")
                return
            # check what we have to the left
            leftElement = other.parent.children[indx-1]
            if isinstance(leftElement, Superscript): 
                print("leftElement is superscript")
                return
            if isinstance(leftElement, SuperSubscript): 
                print("leftElement is supersubscript")
                return
            if isinstance(leftElement, Subscript): 
                print("leftElement is subscript")
                return
            print("leftElement is not a superscript, supersubscript or subscript")
            return
                
        # check if we are at the end of the base of a script
        if cursorPosition == len(other.text()):
            if isinstance(other.parent, subscript.Base):
                print("at the end of subscript base")
                return
            if isinstance(other.parent, supersubscript.Base):
                print("at the end of supersubscript base")
                return
            if isinstance(other.parent, superscript.Base):
                print("at the end of superscript base")
                return

        print("in the middle of a lineEdit")


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
