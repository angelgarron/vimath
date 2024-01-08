from base import RegisterAction
from scene import scene
from PySide6.QtGui import Qt


symbols = {
"a": "α",
"b": "β",
"G": "Γ",
"g": "γ",
"D": "Δ",
"d": "δ",
"e": "ε",
"z": "ζ",
# "η",
"v": "θ",
# "ι",
"k": "κ",
"L": "Λ",
"l": "λ",
"m": "μ",
"n": "ν",
# "Ξ",
# "ξ",
"P": "Π",
"p": "π",
"r": "ρ",
"S": "Σ",
"s": "σ",
"t": "τ",
# "υ",
# "Φ",
# "φ",
# "χ",
# "Ψ",
# "ψ",
"O": "Ω",
"o": "ω",
}


class AddSymbol:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_G, self.lastKey]

        
    def performAction(self, other):
        cursorPosition = other.cursorPosition()
        text = other.text()
        text = list(text)
        text.insert(cursorPosition, symbols[self.symbol])
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
