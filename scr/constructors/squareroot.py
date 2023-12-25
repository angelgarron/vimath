from frame import MyFrame


class SquareRoot(MyFrame):
    VSPACE = 3
    LHSPACE = 8
    RHSPACE = 3
    def __init__(self, parent):
        super().__init__(parent)
        self.squareRootArgumentFrame = MyFrame(self)
        self.children.append(self.squareRootArgumentFrame)


    def setFirstLineEdit(self):
        self.squareRootArgumentFrame.setFirstLineEdit()

        
    @property
    def firstLinedit(self):
        return self.squareRootArgumentFrame.firstLinedit
    

    @property
    def lastLinedit(self):
        return self.squareRootArgumentFrame.lastLinedit


    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.squareRootArgumentFrame.firstLinedit.upperLinedit = currentLinedit.upperLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit
        self.squareRootArgumentFrame.firstLinedit.lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit


    def updateFrameSizeAndPosition(self):
        self.squareRootArgumentFrame.updateFrameSizeAndPosition()
        self.u = self.squareRootArgumentFrame.u+2*SquareRoot.VSPACE
        self.d = self.squareRootArgumentFrame.d+SquareRoot.VSPACE
        width = self.squareRootArgumentFrame.width()+SquareRoot.LHSPACE+SquareRoot.RHSPACE
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        self.squareRootArgumentFrame.setGeometry(SquareRoot.LHSPACE, 2*SquareRoot.VSPACE, self.squareRootArgumentFrame.width(), self.squareRootArgumentFrame.height())


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = self.createPainter()
        painter.drawLine(0, 2*self.height()/3, 2*SquareRoot.LHSPACE/3, self.height())
        painter.drawLine(2*SquareRoot.LHSPACE/3, self.height(), SquareRoot.LHSPACE, SquareRoot.VSPACE)
        painter.drawLine(SquareRoot.LHSPACE, SquareRoot.VSPACE, self.width(), SquareRoot.VSPACE)


    def deserialize(self, data):
        self.squareRootArgumentFrame.deserialize(data[0]["elements"])
