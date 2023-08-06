import sys
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QKeySequence, QShortcut, QTextCursor)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout)


class MyTextEdit(QTextEdit):
    movements = {
        Qt.Key_H:QTextCursor.MoveOperation.PreviousCharacter, 
        Qt.Key_J:QTextCursor.MoveOperation.Down, 
        Qt.Key_K:QTextCursor.MoveOperation.Up, 
        Qt.Key_L:QTextCursor.MoveOperation.NextCharacter, 
        Qt.Key_B:QTextCursor.MoveOperation.PreviousWord, 
        Qt.Key_W:QTextCursor.MoveOperation.NextWord, 
        Qt.Key_E:[
            QTextCursor.MoveOperation.NextWord, 
            QTextCursor.MoveOperation.EndOfWord, 
            #  QTextCursor.MoveOperation.PreviousCharacter
            ], 
        }

    def __init__(self):
        super().__init__()
        self.cursor = self.textCursor()
        self.cursor.insertText("one two three\nfour five six")
        self.setFont("monospace")
        self.setCursorWidth(8)
        self.insertMode = False

    def keyPressEvent(self, event):
        if self.insertMode:
            if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                self.exitInsertMode()
            else:
                super().keyPressEvent(event)
        else:
            if event.text() == "i" and not self.insertMode:
                self.enterInsertMode()
            else:
                if event.key() in self.movements.keys():
                    self.moveCursor(event.key())

    def enterInsertMode(self):
        self.insertMode = True
        self.setCursorWidth(1)

    def exitInsertMode(self):
        self.insertMode = False
        self.setCursorWidth(8)

    def moveCursor(self, key):
        movement = self.movements[key]
        if isinstance(key, list):
            for m in movement:
                self.cursor.movePosition(m, self.cursor.MoveMode.MoveAnchor, 1)
                self.setTextCursor(self.cursor)
        else:
            self.cursor.movePosition(movement, self.cursor.MoveMode.MoveAnchor, 1)
            self.setTextCursor(self.cursor)
            

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
