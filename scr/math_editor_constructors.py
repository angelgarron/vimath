class Fraction(MyFrame):
    VSPACE = 3
    HSPACE = 5
    def __init__(self, parent):
        super().__init__(parent)
        self.numerator = MyFrame(self.graphicsFrame)
        self.denominator = MyFrame(self.graphicsFrame)
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
        lenFractionLine = max(self.numerator.graphicsFrame.width(), self.denominator.graphicsFrame.width())+2*Fraction.HSPACE
        self.u = self.numerator.graphicsFrame.height()+Fraction.VSPACE
        self.d = self.denominator.graphicsFrame.height()+Fraction.VSPACE
        self.graphicsFrame.setGeometry(QRect(self.graphicsFrame.x(), self.graphicsFrame.y(), lenFractionLine, self.u+self.d))
        xn = (self.graphicsFrame.width()-self.numerator.graphicsFrame.width())/2
        yn = 0
        xd = (self.graphicsFrame.width()-self.denominator.graphicsFrame.width())/2
        yd = self.u+Fraction.VSPACE
        self.numerator.graphicsFrame.setGeometry(QRect(xn, yn, self.numerator.graphicsFrame.width(), self.numerator.graphicsFrame.height()))
        self.denominator.graphicsFrame.setGeometry(QRect(xd, yd, self.denominator.graphicsFrame.width(), self.denominator.graphicsFrame.height()))


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = self.createPainter()
        painter.drawLine(0, self.u, self.width(), self.u)


class SquareRoot(MyFrame):
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


class Subscript(MyFrame):
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


class Superscript(MyFrame):
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


class SuperSubscript(MyFrame):
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


class Parenthesis(MyFrame):
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