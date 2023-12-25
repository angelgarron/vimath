from frame import MyFrame


class Numerator(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLinedit(self):
        return self.parent.nextLinedit
    

    @property
    def previousLinedit(self):
        return self.parent.previousLinedit
    

    @property
    def lowerLinedit(self):
        return self.parent.denominator.firstLinedit


class Denominator(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLinedit(self):
        return self.parent.nextLinedit
    

    @property
    def previousLinedit(self):
        return self.parent.previousLinedit
    

    @property
    def upperLinedit(self):
        return self.parent.numerator.firstLinedit


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
    def firstLinedit(self):
        return self.numerator.firstLinedit
    

    @property
    def lastLinedit(self):
        return self.numerator.lastLinedit


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
        painter = self.createPainter()
        painter.drawLine(0, self.u, self.width(), self.u)
        
        
    def deserialize(self, data):
        self.numerator.deserialize(data[0]["elements"])
        self.denominator.deserialize(data[1]["elements"])
