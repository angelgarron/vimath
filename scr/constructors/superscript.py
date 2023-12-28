from frame import MyFrame


class Superior(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLinedit(self):
        return self.parent.nextLinedit
    

    @property
    def previousLinedit(self):
        return self.parent.base.lastLinedit
    

    @property
    def lowerLinedit(self):
        return self.parent.base.firstLinedit


class Base(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLinedit(self):
        return self.parent.nextLinedit
    

    @property
    def previousLinedit(self):
        return self.parent.previousLinedit
    

    @property
    def upperLinedit(self):
        return self.parent.superscript.firstLinedit


class Superscript(MyFrame):
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.base = Base(self)
        self.superscript = Superior(self)
        self.children.append(self.superscript)
        self.children.append(self.base)
        

    def setFirstLineEdit(self):
        self.base.setFirstLineEdit()
        self.superscript.setFirstLineEdit()


    @property
    def firstLinedit(self):
        return self.base.firstLinedit
    

    @property
    def lastLinedit(self):
        return self.base.lastLinedit

    
    def updateFrameSizeAndPosition(self):
        self.base.updateFrameSizeAndPosition()
        self.superscript.updateFrameSizeAndPosition()
        self.d = self.base.d
        superscriptGap = max(Superscript.VSPACE, self.superscript.d-self.base.u)
        self.u = self.superscript.u+superscriptGap+self.base.u
        width = self.base.width()+self.superscript.width()
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        xi = self.base.width()
        yb = self.superscript.u+superscriptGap
        self.base.setGeometry(0, yb, self.base.width(), self.base.height())
        self.superscript.setGeometry(xi, 0, self.superscript.width(), self.superscript.height())
