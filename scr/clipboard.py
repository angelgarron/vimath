from lineedit import MyLineEdit


class Clipboard:
    def __init__(self, scene):
        self.scene = scene
        self.clipboardElements = []
    
    
    def serializeSelected(self):
        self.clipboardElements = []

        first = self.scene.selection[0]
        second = self.scene.selection[-1]
        
        if first[0] == second[0]: # we are in the same lineEdit
            self.clipboardElements.append(first[0].serialize(first[1], second[1]))
            print("the serialized elements are", self.clipboardElements)
            return

        start, end = 1, -1
        if not isinstance(first[0], MyLineEdit):
            start = 0
        if not isinstance(second[0], MyLineEdit):
            end = None

        if isinstance(first[0], MyLineEdit):
            self.clipboardElements.append(first[0].serialize(first[1], None))

        for i, s in enumerate(self.scene.selection[start:end]):
            if i%2 != 0:
                self.clipboardElements.append(s[0].serialize())
            else:
                self.clipboardElements.append(s[0].serialize())

        if isinstance(second[0], MyLineEdit):
            self.clipboardElements.append(second[0].serialize(None, second[1]))

        print("the serialized elements are", self.clipboardElements)


    def deserializeFromClipboard(self):
        leftLineEdit = self.scene.getLineEditWithFocus()
        cursorPosition = leftLineEdit.cursorPosition()

        leftText = leftLineEdit.text()[:cursorPosition]
        rightText = leftLineEdit.text()[cursorPosition:]
        
        clipboardElements = self.clipboardElements.copy()
        if not self.scene.returnClass[clipboardElements[0]["constructor"]] == MyLineEdit:
            clipboardElements.insert(0, {"constructor":str(MyLineEdit), "text": ""})
        if not self.scene.returnClass[clipboardElements[-1]["constructor"]] == MyLineEdit:
            clipboardElements.append({"constructor":str(MyLineEdit), "text": ""})

        if len(clipboardElements) == 1: # just one lineEdit
            leftLineEdit.setText(leftText+clipboardElements[0]["text"]+rightText)
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
