from frame import MyFrame


class Line(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLineEdit(self):
        return self.parent.nextLineEdit
    

    @property
    def previousLineEdit(self):
        return self.parent.previousLineEdit
    

    @property
    def lowerLineEdit(self):
        indx = self.parent.children.index(self)
        if indx+2 > len(self.parent.children):
            return
        return self.parent.children[indx+1].firstLineEdit


    @property
    def upperLineEdit(self):
        indx = self.parent.children.index(self)
        if indx == 0:
            return
        return self.parent.children[indx-1].firstLineEdit

        
    def removeLine(self):
        if self.lineNumber+1 == len(self.parent.children): # we are in the last line
            if self.lineNumber == 0: # there is only one line
                self.scene.clearLine(self)
                return
            lineEditToFocus = self.upperLineEdit
        else:
            lineEditToFocus = self.lowerLineEdit
        self.scene.clearLine(self)
        self.firstLineEdit.deleteLater()
        self.deleteLater()
        self.parent.children.remove(self)
        lineEditToFocus.setFocus()
        self.scene.updateFrames()

        
    @property
    def lineNumber(self):
        return self.parent.children.index(self)


class MainFrame(MyFrame):
    HSPACE = 10
    VSPACE = 10
    def __init__(self, parent):
        super().__init__(parent)
        self.createLine()

        
    def createLine(self, position=None):
        if position is None:
            position = len(self.children)
        line = Line(self)
        line.setFirstLineEdit()
        self.children.insert(position, line)
        self.scene.updateFrames()
        return line
        
        
    @property
    def firstLineEdit(self):
        return self.children[0].firstLineEdit
    

    @property
    def lastLineEdit(self):
        return self.children[0].lastLineEdit


    def updateFrameSizeAndPosition(self):
        height = 0
        y = 0
        maxWidthLines = 0
        for line in self.children:
            line.updateFrameSizeAndPosition()
            height += line.height()+MainFrame.VSPACE
            line.setGeometry(0, y, line.width(), line.height())
            y += line.height()+MainFrame.VSPACE
            maxWidthLines = max(maxWidthLines, line.width())
        self.setGeometry(MainFrame.HSPACE, 0, maxWidthLines, height)


    def removeFrame(self):
        line = self.scene.getLineEditWithFocus().parent
        line.removeLine()
