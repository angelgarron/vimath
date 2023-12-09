from frame import MyFrame, BaseFrame
from PySide6.QtCore import QRect


class SuperSubscript(BaseFrame):
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
