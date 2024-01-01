from frame import MyFrame


class Line(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLinedit(self):
        return self.parent.nextLinedit
    

    @property
    def previousLinedit(self):
        return self.parent.previousLinedit
    

    @property
    def lowerLinedit(self):
        indx = self.parent.children.index(self)
        if indx+2 > len(self.parent.children):
            return
        return self.parent.children[indx+1].firstLinedit


    @property
    def upperLinedit(self):
        indx = self.parent.children.index(self)
        if indx == 0:
            return
        return self.parent.children[indx-1].firstLinedit

        
    def removeLine(self):
        indx = self.parent.children.index(self)
        if indx+1 == len(self.parent.children): # we are in the last line
            if indx == 0: # there is only one line
                self.scene.clearLine(self)
                return
            self.upperLinedit.setFocus()
        else:
            self.lowerLinedit.setFocus()
        self.scene.clearLine(self)
        self.firstLinedit.deleteLater()
        self.scene.removeLineEdit(self.firstLinedit)
        self.deleteLater()
        self.scene.removeFrame(self)
        self.parent.children.remove(self)
        self.scene.updateFrames()


class MainFrame(MyFrame):
    VSPACE = 3
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
    def firstLinedit(self):
        return self.children[0].firstLinedit
    

    @property
    def lastLinedit(self):
        return self.children[0].lastLinedit


    def updateFrameSizeAndPosition(self):
        height = 0
        y = 0
        for line in self.children:
            line.updateFrameSizeAndPosition()
            height += line.height()+MainFrame.VSPACE
            line.setGeometry(0, y, line.width(), line.height())
            y += line.height()+MainFrame.VSPACE
        self.setGeometry(0, 0, 500, height)


    def deserialize(self, data):
        for i, line in enumerate(self.children):
            line.deserialize(data[i]["elements"])
