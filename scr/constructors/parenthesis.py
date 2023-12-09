from frame import MyFrame, BaseFrame
from PySide6.QtCore import QRect


class Parenthesis(BaseFrame):
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
