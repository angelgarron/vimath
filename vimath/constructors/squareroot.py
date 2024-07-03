from vimath.frame import MyFrame
from PySide6.QtGui import QPainter


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
    def firstLineEdit(self):
        return self.squareRootArgumentFrame.firstLineEdit
    

    @property
    def lastLineEdit(self):
        return self.squareRootArgumentFrame.lastLineEdit


    def updateFrameSizeAndPosition(self):
        self.squareRootArgumentFrame.updateFrameSizeAndPosition()
        self.u = self.squareRootArgumentFrame.u+2*SquareRoot.VSPACE
        self.d = self.squareRootArgumentFrame.d+SquareRoot.VSPACE
        width = self.squareRootArgumentFrame.width()+SquareRoot.LHSPACE+SquareRoot.RHSPACE
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        self.squareRootArgumentFrame.setGeometry(SquareRoot.LHSPACE, 2*SquareRoot.VSPACE, self.squareRootArgumentFrame.width(), self.squareRootArgumentFrame.height())


    def paintEvent(self, event):
        super().paintEvent(event)
        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.drawLine(0, 2*self.height()/3, 2*SquareRoot.LHSPACE/3, self.height())
            painter.drawLine(2*SquareRoot.LHSPACE/3, self.height(), SquareRoot.LHSPACE, SquareRoot.VSPACE)
            painter.drawLine(SquareRoot.LHSPACE, SquareRoot.VSPACE, self.width(), SquareRoot.VSPACE)


    def deserialize(self, data):
        self.squareRootArgumentFrame.deserialize(data[0]["elements"])
