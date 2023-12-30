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


@RegisterAction("visual")
class CreateSquareRootAround:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_S]

        
    def performAction(self, other):
        register = []
        scene.clipboard.serializeSelected(scene.selection, register)
        newFrame = other.createFrameMiddle(SquareRoot, storeHistory=False)
        scene.deleteSelection()
        newFrame.squareRootArgumentFrame.firstLinedit.setFocus()
        scene.clipboard.deserializeFromClipboard(register)
        scene.enterNormalMode()


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
            element.subscript.firstLinedit.setFocus()
            return
        if isinstance(other.parent, supersubscript.Base):
            element.subscript.firstLinedit.setFocus()
            return
        if isinstance(other.parent, subscript.Base):
            element.subscript.firstLinedit.setFocus()
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
                leftElement.subscript.firstLinedit.setFocus()
                return
            if isinstance(leftElement, SuperSubscript): 
                leftElement.subscript.firstLinedit.setFocus()
                return
            if isinstance(leftElement, Superscript): 
                leftElement.__class__ = SuperSubscript
                leftElement.base.__class__ = supersubscript.Base
                leftElement.subscript = supersubscript.Inferior(leftElement)
                leftElement.subscript.setFirstLineEdit()
                leftElement.children.append(leftElement.subscript)
                leftElement.superscript.__class__ = supersubscript.Superior
                scene.updateFrames()
                leftElement.subscript.firstLinedit.setFocus()
                return
            selection = [(leftElement, None)]
            register = []
            scene.clipboard.serializeSelected(selection, register)
            newFrame = other.createFrameMiddle(Subscript, storeHistory=False)
            leftElement.removeFrame()
            newFrame.base.firstLinedit.setFocus()
            scene.clipboard.deserializeFromClipboard(register)
            newFrame.subscript.firstLinedit.setFocus()
            return
                
        # we are in the middle of a lineEdit
        newFrame = other.createFrameMiddle(Subscript, storeHistory=False)
        characterLeft = other.text()[-1]
        newFrame.base.firstLinedit.setText(characterLeft)
        other.setText(other.text()[:-1])
        newFrame.subscript.firstLinedit.setFocus()


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
            element.superscript.firstLinedit.setFocus()
            return
        if isinstance(other.parent, supersubscript.Base):
            element.superscript.firstLinedit.setFocus()
            return
        if isinstance(other.parent, superscript.Base):
            element.superscript.firstLinedit.setFocus()
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
                leftElement.superscript.firstLinedit.setFocus()
                return
            if isinstance(leftElement, SuperSubscript): 
                leftElement.superscript.firstLinedit.setFocus()
                return
            if isinstance(leftElement, Subscript): 
                leftElement.__class__ = SuperSubscript
                leftElement.base.__class__ = supersubscript.Base
                leftElement.superscript = supersubscript.Superior(leftElement)
                leftElement.superscript.setFirstLineEdit()
                leftElement.children.insert(0, leftElement.superscript)
                leftElement.subscript.__class__ = supersubscript.Inferior
                scene.updateFrames()
                leftElement.superscript.firstLinedit.setFocus()
                return
            selection = [(leftElement, None)]
            register = []
            scene.clipboard.serializeSelected(selection, register)
            newFrame = other.createFrameMiddle(Superscript, storeHistory=False)
            leftElement.removeFrame()
            newFrame.base.firstLinedit.setFocus()
            scene.clipboard.deserializeFromClipboard(register)
            newFrame.superscript.firstLinedit.setFocus()
            return
                
        # we are in the middle of a lineEdit
        newFrame = other.createFrameMiddle(Superscript, storeHistory=False)
        characterLeft = other.text()[-1]
        newFrame.base.firstLinedit.setText(characterLeft)
        other.setText(other.text()[:-1])
        newFrame.superscript.firstLinedit.setFocus()


@RegisterAction("normal")
class CreateParenthesis:
    def __init__(self):
        self.key = [Qt.ShiftModifier | Qt.Key_ParenLeft]

        
    def performAction(self, other):
        other.createFrameMiddle(Parenthesis)
