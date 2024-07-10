from vimath.base import RegisterAction
from vimath.scene import scene
from PySide6.QtGui import Qt
from vimath.utils import symbols


class AddSymbol:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_G, self.lastKey]

        
    def performAction(self, other):
        other.text().insertTextOnCursorPosition(symbols[self.symbol])
        other.scene.updateFrames()


for symbol in symbols:
    lastKey = getattr(Qt, "Key_"+symbol.upper())
    if symbol.isupper():
        lastKey = Qt.ShiftModifier | lastKey
    newConstructor = type(
        f"{symbol}AddSymbol",
        (AddSymbol, ),
        {
            "lastKey": lastKey,
            "symbol": symbol
        }
    )
    RegisterAction(["normal", "insert"])(newConstructor)
