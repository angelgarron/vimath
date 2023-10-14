from base import actions, actionsVisual, actionsInsert
from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import QRect, Qt, QSize

LINEDIT_SIZE = (8, 20)
CURSOR_WIDTH = 12
LINEDIT_STYLESHEET = """
color: black;
border: 1px solid gray;
border-radius: 4px;
background: transparent;
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
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        # normal:0, insert:1, visual:2
        self.mode = 0
        self.storedKeys = []
        self.actions = actions
        self.actionsVisual = actionsVisual

        self.setFont(QFont("monospace", self.parent.fontSize))
        self.u = self.parent.fontSize/2+2
        self.d = self.parent.fontSize/2+2
        self.setGeometry(QRect(0, 0, LINEDIT_SIZE[0], self.u+self.d))

        self.nextLinedit = None
        self.previousLinedit = None
        self.upperLinedit = None
        self.lowerLinedit = None

        self.textChanged.connect(self.updateWidth)
        self.textEdited.connect(self.wasEdited)
        self.updateWidth()

        
    def wasEdited(self):
        text = self.text()
        for action in actionsInsert.values():
            cursorPosition = text.find(action.key[0])
            if cursorPosition != -1:
                action.performAction(self, cursorPosition, text)


    def updateWidth(self):
        width = self.fontMetrics().horizontalAdvance(self.text())
        self.setFixedWidth(width+8)
        tight = self.fontMetrics().tightBoundingRect(self.text())
        self.setFixedHeight(tight.height()+6)
        self.setTextMargins(0, -tight.top()-self.font().pointSize()-2, 0, 0)
        self.u = -tight.top()
        self.d = self.height()-self.u
        self.setGeometry(self.x(), self.y(), self.width(), self.u+self.d)
        MyFrame.updateFrames()
        

    def keyPressEvent(self, event):
        if event.keyCombination() == Qt.ControlModifier | Qt.Key_C:
            self.storedKeys = []
            if self.mode != 0:
                self.enterNormalMode()
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
        self.fontSize = self.parent.fontSize
        self.setFont(QFont("monospace", self.fontSize))
        self.setStyleSheet("border:1px dashed red")

        
    def createFrameMiddle(self, currentLinedit, FrameConstructor):
        cursorPosition = currentLinedit.cursorPosition()
        newFrame = FrameConstructor(self)
        currentLineditPosition = self.children.index(currentLinedit)
        self.children.insert(currentLineditPosition, newFrame)
        newLinedit = self.createLineEdit(currentLineditPosition)
        newLinedit.setText(currentLinedit.text()[:cursorPosition])
        currentLinedit.setText(currentLinedit.text()[cursorPosition:])
        newFrame.createLinks(newLinedit, currentLinedit)
        newFrame.firstLinedit.setFocus()
        return newFrame
        

    def removeFrame(self):
        MyFrame.frames.remove(self)
        indexDeleted = self.parent.children.index(self)
        leftLinedit = self.parent.children[indexDeleted-1]
        rightLinedit = self.parent.children[indexDeleted+1]
        leftText = leftLinedit.text()
        rightText = rightLinedit.text()
        mergedText = leftText+rightText
        rightLinedit.setText(mergedText)
        # give focus to someone else so it doesn't crash when self is deleted
        rightLinedit.setFocus()
        rightLinedit.setCursorPosition(len(leftText))
        rightLinedit.previousLinedit = leftLinedit.previousLinedit
        self.parent.children.remove(leftLinedit)
        leftLinedit.deleteLater()
        self.parent.children.remove(self)
        self.deleteLater()
        return rightLinedit


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
        self.u = 0
        self.d = 0
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
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.baseCharacter = MyFrame(self)
        self.fontSize = 10
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
        subscriptGap = max(Subscript.VSPACE, self.subscript.u-self.baseCharacter.d)
        self.d = self.baseCharacter.d+subscriptGap+self.subscript.d
        width = self.baseCharacter.width()+self.subscript.width()
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
        xi = self.baseCharacter.width()
        yi = self.baseCharacter.height()+subscriptGap-self.subscript.u
        self.baseCharacter.setGeometry(QRect(0, 0, self.baseCharacter.width(), self.baseCharacter.height()))
        self.subscript.setGeometry(QRect(xi, yi, self.subscript.width(), self.subscript.height()))


class Superscript(BaseFrame):
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.baseCharacter = MyFrame(self)
        self.fontSize = 10
        self.superscript = MyFrame(self)
        self.children.append(self.baseCharacter)
        self.children.append(self.superscript)
        self.firstLinedit = self.baseCharacter.children[0]
        
        
    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.superscript.children[0].nextLinedit = currentLinedit
        self.superscript.children[0].previousLinedit = newLinedit
        self.baseCharacter.children[0].upperLinedit = self.superscript.children[0]
        self.superscript.children[0].lowerLinedit = self.baseCharacter.children[0]
        self.superscript.children[0].upperLinedit = currentLinedit.upperLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit
        self.baseCharacter.children[0].lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit


    def updateFrameSizeAndPosition(self):
        self.baseCharacter.updateFrameSizeAndPosition()
        self.superscript.updateFrameSizeAndPosition()
        self.d = self.baseCharacter.d
        superscriptGap = max(Subscript.VSPACE, self.superscript.d-self.baseCharacter.u)
        self.u = self.superscript.u+superscriptGap+self.baseCharacter.u
        width = self.baseCharacter.width()+self.superscript.width()
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
        xi = self.baseCharacter.width()
        yb = self.superscript.u+superscriptGap
        self.baseCharacter.setGeometry(QRect(0, yb, self.baseCharacter.width(), self.baseCharacter.height()))
        self.superscript.setGeometry(QRect(xi, 0, self.superscript.width(), self.superscript.height()))


class SuperSubscript(BaseFrame):
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.baseCharacter = MyFrame(self)
        self.fontSize = 10
        self.superscript = MyFrame(self)
        self.subscript = MyFrame(self)
        self.children.append(self.baseCharacter)
        self.children.append(self.superscript)
        self.firstLinedit = self.baseCharacter.children[0]
        
        
    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.superscript.children[0].nextLinedit = currentLinedit
        self.superscript.children[0].previousLinedit = newLinedit
        self.subscript.children[0].nextLinedit = currentLinedit
        self.subscript.children[0].previousLinedit = newLinedit
        self.baseCharacter.children[0].upperLinedit = self.superscript.children[0]
        self.baseCharacter.children[0].lowerLinedit = self.subscript.children[0]
        self.superscript.children[0].lowerLinedit = self.baseCharacter.children[0]
        self.superscript.children[0].upperLinedit = currentLinedit.upperLinedit
        self.subscript.children[0].lowerLinedit = currentLinedit.lowerLinedit
        self.subscript.children[0].upperLinedit = self.baseCharacter.children[0]
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit


    def updateFrameSizeAndPosition(self):
        self.baseCharacter.updateFrameSizeAndPosition()
        self.superscript.updateFrameSizeAndPosition()
        self.subscript.updateFrameSizeAndPosition()
        superscriptGap = max(SuperSubscript.VSPACE, self.superscript.d-self.baseCharacter.u)
        subscriptGap = max(SuperSubscript.VSPACE, self.subscript.u-self.baseCharacter.d)
        self.u = self.superscript.u+superscriptGap+self.baseCharacter.u
        self.d = self.baseCharacter.d+subscriptGap+self.subscript.d
        width = max(self.baseCharacter.width()+self.superscript.width(),
                    self.baseCharacter.width()+self.subscript.width())
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
        xSuperscript = self.baseCharacter.width()
        xSubscript = self.baseCharacter.width()
        yb = self.superscript.u+superscriptGap
        ySubscript = self.u+self.baseCharacter.d+subscriptGap-self.subscript.u
        self.baseCharacter.setGeometry(QRect(0, yb, self.baseCharacter.width(), self.baseCharacter.height()))
        self.superscript.setGeometry(QRect(xSuperscript, 0, self.superscript.width(), self.superscript.height()))
        self.subscript.setGeometry(QRect(xSubscript, ySubscript, self.subscript.width(), self.subscript.height()))


class Parenthesis(BaseFrame):
    VSPACE = 3
    LHSPACE = 10
    RHSPACE = 10
    def __init__(self, parent):
        super().__init__(parent)
        self.base = MyFrame(self)
        self.children.append(self.base)
        self.firstLinedit = self.base.children[0]


    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.base.children[0].upperLinedit = currentLinedit.upperLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit
        self.base.children[0].lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit


    def updateFrameSizeAndPosition(self):
        self.base.updateFrameSizeAndPosition()
        self.u = self.base.u+Parenthesis.VSPACE
        self.d = self.base.d+Parenthesis.VSPACE
        width = self.base.width()+Parenthesis.LHSPACE+Parenthesis.RHSPACE
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
        self.base.setGeometry(QRect(Parenthesis.LHSPACE, Parenthesis.VSPACE, self.base.width(), self.base.height()))


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = self.createPainter()
        painter.drawArc(4, 0, 19, self.height(), 135*16, 90*16)
        painter.drawArc(self.width()-24, 0, 19, self.height(), -45*16, 90*16)
