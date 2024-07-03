from frame import MyFrame
from lineedit import MyLineEdit


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
        return MyLineEdit.focusOutEvent(super().firstLineEdit, event)


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
    def firstLineEdit(self):
        return self.base.firstLineEdit
    

    @property
    def lastLineEdit(self):
        return self.base.lastLineEdit


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
    

    def deserialize(self, data):
        self.base.deserialize(data[0]["elements"])
        self.subscript.deserialize(data[1]["elements"])
