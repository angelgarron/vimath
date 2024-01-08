from base import RegisterAction
from scene import scene
from PySide6.QtGui import Qt


symbols = {
"a": "α",
"b": "β",
# "g": "Γ",
"g": "γ",
# "Δ",
"d": "δ",
"e": "ε",
"z": "ζ",
# "η",
"v": "θ",
# "ι",
"k": "κ",
# "Λ",
"l": "λ",
"m": "μ",
"n": "ν",
# "Ξ",
# "ξ",
# "Π",
"p": "π",
"r": "ρ",
# "Σ",
"s": "σ",
"t": "τ",
# "υ",
# "Φ",
# "φ",
# "χ",
# "Ψ",
# "ψ",
# "Ω",
"o": "ω",
}

class AddSymbol:
    def __init__(self):
        self.key = [Qt.AltModifier | Qt.Key_M, Qt.Key_G, getattr(Qt, "Key_"+self.symbol.upper())]

        
    def performAction(self, other):
        cursorPosition = other.cursorPosition()
        text = other.text()
        text = list(text)
        text.insert(cursorPosition, symbols[self.symbol])
        text = "".join(text)
        other.setText(text)
        other.setCursorPosition(cursorPosition+1)


for symbol in symbols:
    newConstructor = type(
        f"{symbol}AddSymbol",
        (AddSymbol, ),
        {
            "symbol": symbol
        }
    )
    RegisterAction(["normal", "insert"])(newConstructor)
