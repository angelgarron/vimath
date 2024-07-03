from vimath.base import RegisterAction
from vimath.scene import scene
from PySide6.QtGui import Qt


symbols = {
"a": 174,
"b": 175,
"G": 161,
"g": 176,
"D": 162,
"d": 177,
"e": 34,
"z": 179,
# "η": 180,
"v": 181,
# "ι",
"k": 183,
"L": 164,
"l": 184,
"m": 185,
"n": 186,
# "Ξ",
# "ξ",
"P": 166,
"p": 188,
"r": 189,
"S": 167,
"s": 190,
"t": 191,
# "υ",
# "Φ",
# "φ",
# "χ",
# "Ψ",
# "ψ",
"O": 172,
"o": 33,
}


class AddSymbol:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_G, self.lastKey]

        
    def performAction(self, other):
        cursorPosition = other.cursorPosition()
        text = other.text()
        text = list(text)
        text.insert(cursorPosition, chr(symbols[self.symbol]))
        text = "".join(text)
        other.setText(text)
        other.setCursorPosition(cursorPosition+1)


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
