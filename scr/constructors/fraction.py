from frame import MyFrame
from PySide6.QtGui import QPainter


class Numerator(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLineEdit(self):
        return self.parent.nextLineEdit
    

    @property
    def previousLineEdit(self):
        return self.parent.previousLineEdit
    

    @property
    def lowerLineEdit(self):
        return self.parent.denominator.firstLineEdit


class Denominator(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.emptyWidth = self.fontSize

        
    @property
    def nextLineEdit(self):
        return self.parent.nextLineEdit
    

    @property
    def previousLineEdit(self):
        return self.parent.previousLineEdit
    

    @property
    def upperLineEdit(self):
        return self.parent.numerator.firstLineEdit


class Fraction(MyFrame):
    VSPACE = 3
    HSPACE = 5
    def __init__(self, parent):
        super().__init__(parent)
        self.numerator = Numerator(self)
        self.denominator = Denominator(self)
        self.children.append(self.numerator)
        self.children.append(self.denominator)
        
        
    def setFirstLineEdit(self):
        self.numerator.setFirstLineEdit()
        self.denominator.setFirstLineEdit()


    @property
    def firstLineEdit(self):
        return self.numerator.firstLineEdit
    

    @property
    def lastLineEdit(self):
        return self.numerator.lastLineEdit


    def updateFrameSizeAndPosition(self):
        self.numerator.updateFrameSizeAndPosition()
        self.denominator.updateFrameSizeAndPosition()
        lenFractionLine = max(self.numerator.width(), self.denominator.width())+2*Fraction.HSPACE
        self.u = self.numerator.height()+Fraction.VSPACE
        self.d = self.denominator.height()+Fraction.VSPACE
        self.setGeometry(self.x(), self.y(), lenFractionLine, self.u+self.d)
        xn = (self.width()-self.numerator.width())/2
        yn = 0
        xd = (self.width()-self.denominator.width())/2
        yd = self.u+Fraction.VSPACE
        self.numerator.setGeometry(xn, yn, self.numerator.width(), self.numerator.height())
        self.denominator.setGeometry(xd, yd, self.denominator.width(), self.denominator.height())


    def paintEvent(self, event):
        super().paintEvent(event)
        with QPainter(self) as painter:
            painter.drawLine(0, self.u, self.width(), self.u)
        
        
    def deserialize(self, data):
        self.numerator.deserialize(data[0]["elements"])
        self.denominator.deserialize(data[1]["elements"])
