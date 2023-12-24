from frame import MyFrame


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
        self.firstLinedit = self.baseCharacter.firstLinedit
        
        
    def createLinks(self, newLinedit, currentLinedit):
        super().createLinks(newLinedit, currentLinedit)
        self.superscript.firstLinedit.nextLinedit = currentLinedit
        self.superscript.firstLinedit.previousLinedit = newLinedit
        self.subscript.firstLinedit.nextLinedit = currentLinedit
        self.subscript.firstLinedit.previousLinedit = newLinedit
        self.baseCharacter.firstLinedit.upperLinedit = self.superscript.firstLinedit
        self.baseCharacter.firstLinedit.lowerLinedit = self.subscript.firstLinedit
        self.superscript.firstLinedit.lowerLinedit = self.baseCharacter.firstLinedit
        self.superscript.firstLinedit.upperLinedit = currentLinedit.upperLinedit
        self.subscript.firstLinedit.lowerLinedit = currentLinedit.lowerLinedit
        self.subscript.firstLinedit.upperLinedit = self.baseCharacter.firstLinedit
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
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        xSuperscript = self.baseCharacter.width()
        xSubscript = self.baseCharacter.width()
        yb = self.superscript.u+superscriptGap
        ySubscript = self.u+self.baseCharacter.d+subscriptGap-self.subscript.u
        self.baseCharacter.setGeometry(0, yb, self.baseCharacter.width(), self.baseCharacter.height())
        self.superscript.setGeometry(xSuperscript, 0, self.superscript.width(), self.superscript.height())
        self.subscript.setGeometry(xSubscript, ySubscript, self.subscript.width(), self.subscript.height())
