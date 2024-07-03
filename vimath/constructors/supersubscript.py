from vimath.frame import MyFrame
from vimath.lineedit import MyLineEdit
from vimath.constructors import subscript, superscript

class Superior(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)


    def getFontSize(self):
        if self.parent.fontSize > self.scene.fontSize*0.75*0.75:
            return self.parent.fontSize*0.75
        return self.parent.fontSize

        
    @property
    def nextLineEdit(self):
        return self.parent.nextLineEdit
    

    @property
    def previousLineEdit(self):
        return self.parent.base.lastLineEdit
    

    @property
    def lowerLineEdit(self):
        return self.parent.base.firstLineEdit
    

    @property
    def firstLineEdit(self):
        fl = super().firstLineEdit
        fl.focusOutEvent = self.fo
        return fl


    def fo(self, event):
        if len(self.children) == 1 and len(self.firstLineEdit.text()) == 0:
            pass
            self.parent.__class__ = subscript.Subscript
            self.parent.base.__class__ = subscript.Base
            self.parent.subscript.__class__ = subscript.Inferior
            self.parent.children.remove(self)
            self.deleteLater()
            self.firstLineEdit.deleteLater()
            self.parent.subscript.firstLineEdit.focusOutEvent = lambda event: subscript.Inferior.fo(self.parent.subscript, event)
            self.scene.updateFrames()
        return MyLineEdit.focusOutEvent(super().firstLineEdit, event)


class Base(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    @property
    def nextLineEdit(self):
        return self.parent.nextLineEdit
    

    @property
    def previousLineEdit(self):
        return self.parent.previousLineEdit
    

    @property
    def upperLineEdit(self):
        return self.parent.superscript.firstLineEdit


    @property
    def lowerLineEdit(self):
        return self.parent.subscript.firstLineEdit


class Inferior(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)

        
    def getFontSize(self):
        if self.parent.fontSize > self.scene.fontSize*0.75*0.75:
            return self.parent.fontSize*0.75
        return self.parent.fontSize


    @property
    def nextLineEdit(self):
        return self.parent.nextLineEdit
    

    @property
    def previousLineEdit(self):
        return self.parent.base.lastLineEdit
    

    @property
    def upperLineEdit(self):
        return self.parent.base.firstLineEdit
    

    @property
    def firstLineEdit(self):
        fl = super().firstLineEdit
        fl.focusOutEvent = self.fo
        return fl


    def fo(self, event):
        if len(self.children) == 1 and len(self.firstLineEdit.text()) == 0:
            pass
            self.parent.__class__ = superscript.Superscript
            self.parent.base.__class__ = superscript.Base
            self.parent.superscript.__class__ = superscript.Superior
            self.parent.children.remove(self)
            self.deleteLater()
            self.firstLineEdit.deleteLater()
            self.parent.superscript.firstLineEdit.focusOutEvent = lambda event: superscript.Superior.fo(self.parent.superscript, event)
            self.scene.updateFrames()
        return MyLineEdit.focusOutEvent(super().firstLineEdit, event)


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
    def firstLineEdit(self):
        return self.base.firstLineEdit
    

    @property
    def lastLineEdit(self):
        return self.base.lastLineEdit


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
