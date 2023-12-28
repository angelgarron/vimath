from frame import MyFrame


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
    def lowerLinedit(self):
        return self.parent.subscript.firstLinedit


class Inferior(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLinedit(self):
        return self.parent.nextLinedit
    

    @property
    def previousLinedit(self):
        return self.parent.base.lastLinedit
    

    @property
    def upperLinedit(self):
        return self.parent.base.firstLinedit


class Subscript(MyFrame):
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.base = Base(self)
        self.subscript = Inferior(self)
        self.children.append(self.base)
        self.children.append(self.subscript)
        
    
    def setFirstLineEdit(self):
        self.base.setFirstLineEdit()
        self.subscript.setFirstLineEdit()


    @property
    def firstLinedit(self):
        return self.base.firstLinedit
    

    @property
    def lastLinedit(self):
        return self.base.lastLinedit


    def updateFrameSizeAndPosition(self):
        self.base.updateFrameSizeAndPosition()
        self.subscript.updateFrameSizeAndPosition()
        self.u = self.base.u
        subscriptGap = max(Subscript.VSPACE, self.subscript.u-self.base.d)
        self.d = self.base.d+subscriptGap+self.subscript.d
        width = self.base.width()+self.subscript.width()
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        xi = self.base.width()
        yi = self.base.height()+subscriptGap-self.subscript.u
        self.base.setGeometry(0, 0, self.base.width(), self.base.height())
        self.subscript.setGeometry(xi, yi, self.subscript.width(), self.subscript.height())
