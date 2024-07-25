import sys
from PySide6.QtWidgets import QApplication
from vimath.window import MyMainWindow


STYLE_SHEET = """
* {
    background: white;
    color: black;
}
QFrame {
    background: transparent;
}
QFrame[showBox="true"] {
    border: 1px dashed red;
}
QLineEdit {
    border: transparent;
    background: transparent;
}
"""


def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setStyleSheet(STYLE_SHEET)
    window.show()
    window.selectionRectangle.raise_()
    window.graphicCursor.raise_()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
