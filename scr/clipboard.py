from lineedit import MyLineEdit


class Clipboard:
    def __init__(self, scene):
        self.scene = scene
        self.clipboardElements = []
    
    
    def serializeSelected(self, selection=None, register=None):
        if selection is None:
            selection = self.scene.selection
        if register is None:
            self.clipboardElements = []
            register = self.clipboardElements

        first = selection[0]
        second = selection[-1]
        
        # we are in the same lineEdit
        if isinstance(first[0], MyLineEdit) and isinstance(second[0], MyLineEdit) and first[0] == second[0]:
            register.append(first[0].serialize(first[1], second[1]))
            print("the serialized elements are", register)
            return

        start, end = 1, -1
        if not isinstance(first[0], MyLineEdit):
            start = 0
        if not isinstance(second[0], MyLineEdit):
            end = None

        if isinstance(first[0], MyLineEdit):
            register.append(first[0].serialize(first[1], None))

        for i, s in enumerate(selection[start:end]):
            if i%2 != 0:
                register.append(s[0].serialize())
            else:
                register.append(s[0].serialize())

        if isinstance(second[0], MyLineEdit):
            register.append(second[0].serialize(None, second[1]))

        print("the serialized elements are", register)


    def deserializeFromClipboard(self, register=None):
        if register is None:
            register = self.clipboardElements

        leftLineEdit = self.scene.getLineEditWithFocus()
        cursorPosition = leftLineEdit.cursorPosition()

        leftText = leftLineEdit.text()[:cursorPosition]
        rightText = leftLineEdit.text()[cursorPosition:]
        
        clipboardElements = register.copy()
        if not self.scene.returnClass[clipboardElements[0]["constructor"]] == MyLineEdit:
            clipboardElements.insert(0, {"constructor":str(MyLineEdit), "text": ""})
        if not self.scene.returnClass[clipboardElements[-1]["constructor"]] == MyLineEdit:
            clipboardElements.append({"constructor":str(MyLineEdit), "text": ""})

        if len(clipboardElements) == 1: # just one lineEdit
            leftLineEdit.setText(leftText+clipboardElements[0]["text"]+rightText)
            leftLineEdit.setCursorPosition(cursorPosition)
            return

        leftLineEdit.setText(leftText+clipboardElements[0]["text"])

        indx = leftLineEdit.parent.children.index(leftLineEdit)
        for i, element in enumerate(clipboardElements[1:-1]):
            constructor = self.scene.returnClass[element["constructor"]]
            if constructor != MyLineEdit:
                newFrame = constructor(leftLineEdit.parent)
                leftLineEdit.parent.children.insert(indx+i+1, newFrame)
                newFrame.deserialize(element["elements"])
            else:
                newLineEdit = MyLineEdit(leftLineEdit.parent)
                newLineEdit.setText(element["text"])
                leftLineEdit.parent.children.insert(indx+i+1, newLineEdit)

        rightLineEdit = MyLineEdit(leftLineEdit.parent)
        leftLineEdit.parent.children.insert(indx+2, rightLineEdit)
        rightLineEdit.setText(clipboardElements[-1]["text"]+rightText)
        
        self.scene.updateFrames()
