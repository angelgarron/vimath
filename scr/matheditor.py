from base import actions, actionsVisual
from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import QRect, Qt, QSize

LINEDIT_SIZE = (8, 20)
FONTSIZE = 15
CURSOR_WIDTH = 12
LINEDIT_STYLESHEET = """
color: black;
border: 1px solid gray;
border-radius: 4px;
"""

class ThickCursorStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QProxyStyle.PM_TextCursorWidth:
            return CURSOR_WIDTH

        return super().pixelMetric(metric, option, widget)
        

class MyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setStyle(ThickCursorStyle())
        self.setStyleSheet(LINEDIT_STYLESHEET)
        # normal:0, insert:1, visual:2
        self.mode = 0
        self.storedKeys = []
        self.actions = actions
        self.actionsVisual = actionsVisual

        self.setFont(QFont("monospace", FONTSIZE))
        self.setGeometry(QRect(0, 0, LINEDIT_SIZE[0], LINEDIT_SIZE[1]))
        self.u = self.height()/2
        self.d = self.height()/2

        self.nextLinedit = None
        self.previousLinedit = None
        self.upperLinedit = None
        self.lowerLinedit = None

        self.textChanged.connect(self.updateWidth)


    def updateWidth(self):
        width = self.fontMetrics().horizontalAdvance(self.text())
        self.setFixedWidth(width+8)
        MyFrame.updateFrames()
        

    def keyPressEvent(self, event):
        if event.keyCombination() == Qt.ControlModifier | Qt.Key_C:
            self.enterNormalMode()
            self.storedKeys = []
            return

        if self.mode == 1:
            super().keyPressEvent(event)
            return

        if self.mode == 0:
            actions = self.actions
        else:
            actions = self.actionsVisual

        if event.key() in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]:
            return

        self.storedKeys.append(event.keyCombination())

        for action in actions.values():
            if isinstance(action.key[0], list):
                for key in action.key:
                    if key == self.storedKeys:
                        action.performAction(self)
                        self.storedKeys = []
                        break
            else:
                if action.key == self.storedKeys:
                    action.performAction(self)
                    self.storedKeys = []
                    break

    def enterInsertMode(self):
        self.mode = 1
        self.setStyle(QProxyStyle())

    def enterNormalMode(self):
        self.mode = 0
        self.cursorBackward(False)
        self.setStyle(ThickCursorStyle())

    def enterVisualMode(self):
        self.mode = 2
        self.setStyle(ThickCursorStyle())


class BaseFrame(QFrame):
    frames = []
    def __init__(self, parent=None):
        super().__init__(parent)
        MyFrame.frames.append(self)
        self.parent = parent
        self.children = []
        self.setGeometry(QRect(0, 0, LINEDIT_SIZE[0], LINEDIT_SIZE[1]))
        self.u = 0
        self.d = 0
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("border:1px dashed red")

        
    def createFrameMiddle(self, pos, FrameConstructor):
        # FIXME could be more than one linedit
        currentLinedit = self.findChild(MyLineEdit)
        newFrame = FrameConstructor(self)
        self.children.insert(0, newFrame)
        newLinedit = self.createLineEdit()
        newLinedit.setText(currentLinedit.text()[:pos])
        currentLinedit.setText(currentLinedit.text()[pos:])
        newFrame.createLinks(newLinedit, currentLinedit)
        return newFrame
        

    def createLinks(self, newLinedit, currentLinedit):
        newLinedit.previousLinedit = currentLinedit.previousLinedit
        currentLinedit.previousLinedit = self.firstLinedit
        self.firstLinedit.nextLinedit = currentLinedit
        self.firstLinedit.previousLinedit = newLinedit
        newLinedit.nextLinedit = self.firstLinedit


    @classmethod
    def updateFrames(cls):
        mainFrame = MyFrame.frames[0]
        mainFrame.updateFrameSizeAndPosition()
        

    def updateFrameSizeAndPosition(self):
        for child in self.children:
            if not isinstance(child, MyLineEdit):
                child.updateFrameSizeAndPosition()
            self.u = max(self.u, child.u)
            self.d = max(self.d, child.d)
            
        width = 0
        x = 0
        for child in self.children:
            child.setGeometry(QRect(x, self.u-child.u, child.width(), child.height()))
            width += child.width()
            x += child.width()
        
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
    

    def createLineEdit(self, pos=0):
        newLinedit = MyLineEdit(self)
        newLinedit.show()
        self.children.insert(pos, newLinedit)
        return newLinedit
    

    def createPainter(self):
        painter = QPainter(self)
        pen = QPen()
        pen.setColor("black")
        painter.setPen(pen)
        return painter

        
class MyFrame(BaseFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.firstLinedit = self.createLineEdit()
    

class Fraction(BaseFrame):
    VSPACE = 3
    HSPACE = 5
    def __init__(self, parent):
        super().__init__(parent)
        self.numerator = MyFrame(self)
        self.denominator = MyFrame(self)
        self.children.append(self.numerator)
        self.children.append(self.denominator)
        self.firstLinedit = self.numerator.children[0]
        
        
    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.denominator.children[0].nextLinedit = currentLinedit
        self.denominator.children[0].previousLinedit = newLinedit
        self.numerator.children[0].lowerLinedit = self.denominator.children[0]
        self.denominator.children[0].upperLinedit = self.numerator.children[0]
        self.denominator.children[0].lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit
        self.numerator.children[0].upperLinedit = currentLinedit.upperLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit


    def updateFrameSizeAndPosition(self):
        self.numerator.updateFrameSizeAndPosition()
        self.denominator.updateFrameSizeAndPosition()
        lenFractionLine = max(self.numerator.width(), self.denominator.width())+2*Fraction.HSPACE
        self.u = self.numerator.height()+Fraction.VSPACE
        self.d = self.denominator.height()+Fraction.VSPACE
        self.setGeometry(QRect(self.x(), self.y(), lenFractionLine, self.u+self.d))
        xn = (self.width()-self.numerator.width())/2
        yn = 0
        xd = (self.width()-self.denominator.width())/2
        yd = self.u+Fraction.VSPACE
        self.numerator.setGeometry(QRect(xn, yn, self.numerator.width(), self.numerator.height()))
        self.denominator.setGeometry(QRect(xd, yd, self.denominator.width(), self.denominator.height()))


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = self.createPainter()
        painter.drawLine(0, self.u, self.width(), self.u)


class SquareRoot(BaseFrame):
    VSPACE = 3
    LHSPACE = 8
    RHSPACE = 3
    def __init__(self, parent):
        super().__init__(parent)
        self.squareRootArgumentFrame = MyFrame(self)
        self.children.append(self.squareRootArgumentFrame)
        self.firstLinedit = self.squareRootArgumentFrame.children[0]


    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.squareRootArgumentFrame.children[0].upperLinedit = currentLinedit.upperLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit
        self.squareRootArgumentFrame.children[0].lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit


    def updateFrameSizeAndPosition(self):
        self.squareRootArgumentFrame.updateFrameSizeAndPosition()
        self.u = self.squareRootArgumentFrame.u+2*SquareRoot.VSPACE
        self.d = self.squareRootArgumentFrame.d+SquareRoot.VSPACE
        width = self.squareRootArgumentFrame.width()+SquareRoot.LHSPACE+SquareRoot.RHSPACE
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
        self.squareRootArgumentFrame.setGeometry(QRect(SquareRoot.LHSPACE, 2*SquareRoot.VSPACE, self.squareRootArgumentFrame.width(), self.squareRootArgumentFrame.height()))


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = self.createPainter()
        painter.drawLine(0, 2*self.height()/3, 2*SquareRoot.LHSPACE/3, self.height())
        painter.drawLine(2*SquareRoot.LHSPACE/3, self.height(), SquareRoot.LHSPACE, SquareRoot.VSPACE)
        painter.drawLine(SquareRoot.LHSPACE, SquareRoot.VSPACE, self.width(), SquareRoot.VSPACE)


class Subscript(BaseFrame):
    VSPACE = 1
    def __init__(self, parent):
        super().__init__(parent)
        self.baseCharacter = MyFrame(self)
        self.subscript = MyFrame(self)
        self.children.append(self.baseCharacter)
        self.children.append(self.subscript)
        self.firstLinedit = self.baseCharacter.children[0]
        
        
    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.subscript.children[0].nextLinedit = currentLinedit
        self.subscript.children[0].previousLinedit = newLinedit
        self.baseCharacter.children[0].lowerLinedit = self.subscript.children[0]
        self.subscript.children[0].upperLinedit = self.baseCharacter.children[0]
        self.subscript.children[0].lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit
        self.baseCharacter.children[0].upperLinedit = currentLinedit.upperLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit


    def updateFrameSizeAndPosition(self):
        self.baseCharacter.updateFrameSizeAndPosition()
        self.subscript.updateFrameSizeAndPosition()
        self.u = self.baseCharacter.u
        self.d = self.baseCharacter.d+Subscript.VSPACE+self.subscript.d
        width = self.baseCharacter.width()+self.subscript.width()
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
        xi = self.baseCharacter.width()
        yi = self.baseCharacter.height()+Subscript.VSPACE-self.subscript.u
        self.baseCharacter.setGeometry(QRect(0, 0, self.baseCharacter.width(), self.baseCharacter.height()))
        self.subscript.setGeometry(QRect(xi, yi, self.subscript.width(), self.subscript.height()))
