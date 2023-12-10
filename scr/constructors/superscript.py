from frame import MyFrame, BaseFrame


class Superscript(BaseFrame):
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.baseCharacter = MyFrame(self)
        self.fontSize = 10
        self.superscript = MyFrame(self)
        self.children.append(self.baseCharacter)
        self.children.append(self.superscript)
        self.firstLinedit = self.baseCharacter.firstLinedit
        
        
    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.superscript.firstLinedit.nextLinedit = currentLinedit
        self.superscript.firstLinedit.previousLinedit = newLinedit
        self.baseCharacter.firstLinedit.upperLinedit = self.superscript.firstLinedit
        self.superscript.firstLinedit.lowerLinedit = self.baseCharacter.firstLinedit
        self.superscript.firstLinedit.upperLinedit = currentLinedit.upperLinedit
        newLinedit.lowerLinedit = currentLinedit.lowerLinedit
        self.baseCharacter.firstLinedit.lowerLinedit = currentLinedit.lowerLinedit
        newLinedit.upperLinedit = currentLinedit.upperLinedit


    def updateFrameSizeAndPosition(self):
        self.baseCharacter.updateFrameSizeAndPosition()
        self.superscript.updateFrameSizeAndPosition()
        self.d = self.baseCharacter.d
        superscriptGap = max(Superscript.VSPACE, self.superscript.d-self.baseCharacter.u)
        self.u = self.superscript.u+superscriptGap+self.baseCharacter.u
        width = self.baseCharacter.width()+self.superscript.width()
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        xi = self.baseCharacter.width()
        yb = self.superscript.u+superscriptGap
        self.baseCharacter.setGeometry(0, yb, self.baseCharacter.width(), self.baseCharacter.height())
        self.superscript.setGeometry(xi, 0, self.superscript.width(), self.superscript.height())
