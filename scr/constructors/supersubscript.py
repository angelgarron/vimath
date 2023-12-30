from frame import MyFrame
from lineedit import MyLineEdit
from constructors import subscript
from constructors import superscript

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
    

    @property
    def firstLinedit(self):
        fl = super().firstLinedit
        fl.focusOutEvent = self.fo
        return fl


    def fo(self, event):
        if len(self.children) == 1 and len(self.firstLinedit.text()) == 0:
            pass
            self.parent.__class__ = subscript.Subscript
            self.parent.base.__class__ = subscript.Base
            self.parent.subscript.__class__ = subscript.Inferior
            self.parent.children.remove(self)
            self.scene.removeLineEdit(self.firstLinedit)
            self.scene.removeFrame(self)
            self.deleteLater()
            self.firstLinedit.deleteLater()
            self.parent.subscript.firstLinedit.focusOutEvent = lambda event: subscript.Inferior.fo(self.parent.subscript, event)
            self.scene.updateFrames()
        return super(MyLineEdit, self.firstLinedit).focusOutEvent(event)


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
    

    @property
    def firstLinedit(self):
        fl = super().firstLinedit
        fl.focusOutEvent = self.fo
        return fl


    def fo(self, event):
        if len(self.children) == 1 and len(self.firstLinedit.text()) == 0:
            pass
            self.parent.__class__ = superscript.Superscript
            self.parent.base.__class__ = superscript.Base
            self.parent.superscript.__class__ = superscript.Superior
            self.parent.children.remove(self)
            self.scene.removeLineEdit(self.firstLinedit)
            self.scene.removeFrame(self)
            self.deleteLater()
            self.firstLinedit.deleteLater()
            self.parent.superscript.firstLinedit.focusOutEvent = lambda event: superscript.Superior.fo(self.parent.superscript, event)
            self.scene.updateFrames()
        return super(MyLineEdit, self.firstLinedit).focusOutEvent(event)


class SuperSubscript(MyFrame):
    VSPACE = 0.6
    def __init__(self, parent):
        super().__init__(parent)
        self.superscript = Superior(self)
        self.base = Base(self)
        self.subscript = Inferior(self)
        self.children.append(self.superscript)
        self.children.append(self.base)
        self.children.append(self.subscript)
        

    def setFirstLineEdit(self):
        self.superscript.setFirstLineEdit()
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
        self.superscript.updateFrameSizeAndPosition()
        self.subscript.updateFrameSizeAndPosition()
        superscriptGap = max(SuperSubscript.VSPACE, self.superscript.d-self.base.u)
        subscriptGap = max(SuperSubscript.VSPACE, self.subscript.u-self.base.d)
        self.u = self.superscript.u+superscriptGap+self.base.u
        self.d = self.base.d+subscriptGap+self.subscript.d
        width = max(self.base.width()+self.superscript.width(),
                    self.base.width()+self.subscript.width())
        self.setGeometry(self.x(), self.y(), width, self.u+self.d)
        xSuperscript = self.base.width()
        xSubscript = self.base.width()
        yb = self.superscript.u+superscriptGap
        ySubscript = self.u+self.base.d+subscriptGap-self.subscript.u
        self.base.setGeometry(0, yb, self.base.width(), self.base.height())
        self.superscript.setGeometry(xSuperscript, 0, self.superscript.width(), self.superscript.height())
        self.subscript.setGeometry(xSubscript, ySubscript, self.subscript.width(), self.subscript.height())


    def deserialize(self, data):
        self.superscript.deserialize(data[0]["elements"])
        self.base.deserialize(data[1]["elements"])
        self.subscript.deserialize(data[2]["elements"])
