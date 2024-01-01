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
        return self.parent.children[1].firstLinedit


    @property
    def upperLinedit(self):
        return self.parent.children[0].firstLinedit


class MainFrame(MyFrame):
    VSPACE = 3
    def __init__(self, parent):
        super().__init__(parent)
        self.children.append(Line(self))
        self.children.append(Line(self))
        self.children.append(Line(self))
        
        
    def setFirstLineEdit(self):
        for line in self.children:
            line.setFirstLineEdit()


    @property
    def firstLinedit(self):
        return self.children[0].firstLinedit
    

    @property
    def lastLinedit(self):
        return self.children[0].lastLinedit


    def updateFrameSizeAndPosition(self):
        for line in self.children:
            line.updateFrameSizeAndPosition()
        height = 0
        for line in self.children:
            height += line.height()+MainFrame.VSPACE
        self.setGeometry(0, 0, 500, height)
        y = 0
        for line in self.children:
            line.setGeometry(0, y, line.width(), line.height())
            y += line.height()+MainFrame.VSPACE


    def deserialize(self, data):
        for i, line in enumerate(self.children):
            line.deserialize(data[i]["elements"])
