from frame import MyFrame


class Parenthesis(MyFrame):
    VSPACE = 3
    LHSPACE = 10
    RHSPACE = 10
    def __init__(self, parent):
        super().__init__(parent)
        self.base = MyFrame(self)
        self.children.append(self.base)


    def setFirstLineEdit(self):
        self.base.setFirstLineEdit()

        
    @property
    def firstLinedit(self):
        return self.base.firstLinedit
    

    @property
    def lastLinedit(self):
        return self.base.lastLinedit


    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.base.firstLinedit.upperLinedit = currentLinedit.upperLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit
        self.base.firstLinedit.lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit


    def updateFrameSizeAndPosition(self):
        self.base.updateFrameSizeAndPosition()
        self.u = self.base.u+Parenthesis.VSPACE
        self.d = self.base.d+Parenthesis.VSPACE
        width = self.base.width()+Parenthesis.LHSPACE+Parenthesis.RHSPACE
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        self.base.setGeometry(Parenthesis.LHSPACE, Parenthesis.VSPACE, self.base.width(), self.base.height())


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = self.createPainter()
        painter.drawArc(4, 0, 19, self.height(), 135*16, 90*16)
        painter.drawArc(self.width()-24, 0, 19, self.height(), -45*16, 90*16)
