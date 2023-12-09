from frame import MyFrame, BaseFrame
from PySide6.QtCore import QRect


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
        superscriptGap = max(Superscript.VSPACE, self.superscript.d-self.baseCharacter.u)
        self.u = self.superscript.u+superscriptGap+self.baseCharacter.u
        width = self.baseCharacter.width()+self.superscript.width()
        self.setGeometry(QRect(self.x(), self.y(), width, self.u+self.d))
        xi = self.baseCharacter.width()
        yb = self.superscript.u+superscriptGap
        self.baseCharacter.setGeometry(QRect(0, yb, self.baseCharacter.width(), self.baseCharacter.height()))
        self.superscript.setGeometry(QRect(xi, 0, self.superscript.width(), self.superscript.height()))
