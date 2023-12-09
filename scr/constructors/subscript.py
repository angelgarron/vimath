from frame import MyFrame, BaseFrame
from PySide6.QtCore import QRect


class Subscript(BaseFrame):
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
