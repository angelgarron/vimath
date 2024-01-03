import sys
from PySide6.QtWidgets import QApplication
from window import MyMainWindow


STYLE_SHEET = """
QMainWindow {
    background-color: white;
}
QLineEdit {
    color: black;
    border: 1px solid gray;
    border-radius: 4px;
    background: transparent;
}
QFrame {
    border: 1px dashed red;
}
"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setStyleSheet(STYLE_SHEET)
    window.show()
    window.tp.raise_()
    sys.exit(app.exec())
