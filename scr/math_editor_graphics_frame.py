from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)

class MyGraphicsFrame(QFrame):
    def __init__(self, frame, parent, scene):
        super().__init__(parent)
        self.frame = frame
        self.scene = scene

        
    def updateFrames(self):
        self.frame.updateFrames()