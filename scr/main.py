import sys
from PySide6.QtWidgets import QApplication
from window import MyMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setStyleSheet("background-color:white")
    window.show()
    window.tp.raise_()
    sys.exit(app.exec())