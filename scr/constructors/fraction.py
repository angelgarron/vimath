from frame import MyFrame
from PySide6.QtCore import QRect


class Fraction(MyFrame):
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
