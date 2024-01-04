from frame import MyFrame
from lineedit import MyLineEdit


class Superior(MyFrame):
    def __init__(self, parent):
        super().__init__(parent)
    

    def getFontSize(self):
        if self.parent.fontSize > self.scene.fontSize*0.75*0.75:
            return self.parent.fontSize*0.75
        return self.parent.fontSize

        
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
            indx = self.parent.parent.children.index(self.parent)
            rightLineEditOld = self.parent.parent.children[indx+1]
            selection = []
            for element in self.parent.base.children:
                selection.append((element, None))
            register = []
            self.scene.clipboard.serializeSelected(selection, register)
            self.parent.removeFrame()
            self.scene.clipboard.deserializeFromClipboard(register, up=True)
            if len(selection) == 1 and isinstance(selection[0][0], MyLineEdit):
                rightLineEdit = self.parent.parent.children[indx-1]
                rightLineEdit.setCursorPosition(len(rightLineEdit.text())-len(rightLineEditOld.text()))
            else:
                rightLineEdit = self.parent.parent.children[indx+1]
                rightLineEdit.setCursorPosition(0)
            rightLineEdit.setFocus()
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


    def deserialize(self, data):
        self.superscript.deserialize(data[0]["elements"])
        self.base.deserialize(data[1]["elements"])
