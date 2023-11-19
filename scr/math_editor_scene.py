NORMAL_MODE = 0
INSERT_MODE = 1
VISULAL_MODE = 2

class Scene:
    def __init__(self):
        self.mode = NORMAL_MODE
        self.frames = []
        self.lineEdits = []

        
    def addFrame(self, frame):
        self.frames.append(frame)
    

    def addLineEdit(self, lineEdit):
        self.lineEdits.append(lineEdit)
    

    def removeFrame(self, frame):
        self.frames.remove(frame)
    

    def removeLineEdit(self, lineEdit):
        self.lineEdits.remove(lineEdit)