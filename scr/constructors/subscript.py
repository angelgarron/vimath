from frame import MyFrame, BaseFrame


class Subscript(BaseFrame):
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.baseCharacter = MyFrame(self)
        self.fontSize = 10
        self.subscript = MyFrame(self)
        self.children.append(self.baseCharacter)
        self.children.append(self.subscript)
        self.firstLinedit = self.baseCharacter.firstLinedit
        
        
    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.subscript.firstLinedit.nextLinedit = currentLinedit
        self.subscript.firstLinedit.previousLinedit = newLinedit
        self.baseCharacter.firstLinedit.lowerLinedit = self.subscript.firstLinedit
        self.subscript.firstLinedit.upperLinedit = self.baseCharacter.firstLinedit
        self.subscript.firstLinedit.lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit
        self.baseCharacter.firstLinedit.upperLinedit = currentLinedit.upperLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit


    def updateFrameSizeAndPosition(self):
        self.baseCharacter.updateFrameSizeAndPosition()
        self.subscript.updateFrameSizeAndPosition()
        self.u = self.baseCharacter.u
        subscriptGap = max(Subscript.VSPACE, self.subscript.u-self.baseCharacter.d)
        self.d = self.baseCharacter.d+subscriptGap+self.subscript.d
        width = self.baseCharacter.width()+self.subscript.width()
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        xi = self.baseCharacter.width()
        yi = self.baseCharacter.height()+subscriptGap-self.subscript.u
        self.baseCharacter.setGeometry(0, 0, self.baseCharacter.width(), self.baseCharacter.height())
        self.subscript.setGeometry(xi, yi, self.subscript.width(), self.subscript.height())
