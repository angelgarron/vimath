import sys
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QKeySequence, QShortcut, QTextCursor)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout)

movements = {
    "h":QTextCursor.MoveOperation.PreviousCharacter, 
    "j":QTextCursor.MoveOperation.Down, 
    "k":QTextCursor.MoveOperation.Up, 
    "l":QTextCursor.MoveOperation.NextCharacter, 
    "b":QTextCursor.MoveOperation.PreviousWord, 
    "w":QTextCursor.MoveOperation.NextWord, 
    "e":[
        QTextCursor.MoveOperation.NextWord, 
         QTextCursor.MoveOperation.EndOfWord, 
        #  QTextCursor.MoveOperation.PreviousCharacter
         ], 
    }


class MyTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.cursor = self.textCursor()
        self.cursor.insertText("one two three\nfour five six")
        self.setFont("monospace")
        self.setCursorWidth(8)
        self.insertMode = False

    def keyPressEvent(self, event):
        if event.text() == "i" and not self.insertMode:
            self.enterInsertMode()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.exitInsertMode()
        elif not self.insertMode:
            if event.text() in movements.keys():
                self.moveCursor(event.text())
            else:
                pass
        else:
            super().keyPressEvent(event)

    def enterInsertMode(self):
        self.insertMode = True
        self.setCursorWidth(1)

    def exitInsertMode(self):
        self.insertMode = False
        self.setCursorWidth(8)

    def moveCursor(self, char):
        movement = movements[char]
        if isinstance(movement, list):
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
