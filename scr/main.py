import sys
from PySide6.QtWidgets import QApplication
from math_editor_window import MyMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setStyleSheet("background-color:white")
    window.show()
    sys.exit(app.exec())