import sys
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QKeySequence, QShortcut, QTextCursor)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout)
from motion import RegisterAction

class MyTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.cursor = self.textCursor()
        self.cursor.insertText("one two three\nfour five six")
        self.setFont("monospace")
        self.setCursorWidth(8)
        self.insertMode = False
        self.storedKeys = []

    def keyPressEvent(self, event):
        if self.insertMode:
            if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                self.exitInsertMode()
            else:
                super().keyPressEvent(event)
        else:
            if event.key() == Qt.Key_I and not self.insertMode:
                self.enterInsertMode()
            else:
                actions = RegisterAction.actions
                self.storedKeys.append(event.key())
                for action in actions:
                    if action.key == self.storedKeys:
                        action.moveCursor(self.cursor)
                        self.setTextCursor(self.cursor)
                        self.storedKeys = []
                        break

    def enterInsertMode(self):
        self.insertMode = True
        self.setCursorWidth(1)

    def exitInsertMode(self):
        self.insertMode = False
        self.setCursorWidth(8)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        text_edit = MyTextEdit()
        layout.addWidget(text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
