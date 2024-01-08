from base import RegisterAction
from scene import scene
from PySide6.QtGui import Qt


symbols = {
    "p": "π",
}


@RegisterAction(["normal", "insert"])
class AddSymbol:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_G, getattr(Qt, "Key_"+"p".upper())]

        
    def performAction(self, other):
        cursorPosition = other.cursorPosition()
        text = other.text()
        text = list(text)
        text.insert(cursorPosition, symbols["p"])
        text = "".join(text)
        other.setText(text)
        other.setCursorPosition(cursorPosition+1)
