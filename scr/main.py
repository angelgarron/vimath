import sys
from PySide6.QtWidgets import QApplication
from window import MyMainWindow


STYLE_SHEET = """
* {
    background: white;
    color: black;
}
QFrame {
    background: transparent;
}
QLineEdit {
    border: transparent;
}
"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setStyleSheet(STYLE_SHEET)
    window.show()
    window.tp.raise_()
    sys.exit(app.exec())
