import sys
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QKeySequence, QShortcut, QTextCursor)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout)

class RegisterAction(object):
    actions = []
    def __init__(self, action):
        RegisterAction.actions.append(action())

class BaseMovement:
    def moveCursor(self, cursor):
        if isinstance(self.movement, list):
            for m in self.movement:
                cursor.movePosition(m, cursor.MoveMode.MoveAnchor, 1)
        else:
            cursor.movePosition(self.movement, cursor.MoveMode.MoveAnchor, 1)
            
@RegisterAction
class MoveLeft(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_H]
        self.movement = QTextCursor.MoveOperation.PreviousCharacter

@RegisterAction
class MoveDown(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_J]
        self.movement = QTextCursor.MoveOperation.Down

@RegisterAction
class MoveUp(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_K]
        self.movement = QTextCursor.MoveOperation.Up
        
@RegisterAction
class MoveRight(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_L]
        self.movement = QTextCursor.MoveOperation.Right

@RegisterAction
class MoveWordBegin(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_W]
        self.movement = QTextCursor.MoveOperation.NextWord
        
        
@RegisterAction
class MoveBeginningWord(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_B]
        self.movement = QTextCursor.MoveOperation.PreviousWord

@RegisterAction
class MoveWordEnd(BaseMovement):
    def __init__(self):
        self.key = [Qt.Key_E]
        self.movement = [
    QTextCursor.MoveOperation.NextWord, 
    QTextCursor.MoveOperation.EndOfWord, 
    #  QTextCursor.MoveOperation.PreviousCharacter
    ]

class MyTextEdit(QTextEdit):
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
            if event.key() == Qt.Key_I and not self.insertMode:
                self.enterInsertMode()
            else:
                actions = RegisterAction.actions
                for action in actions:
                    if event.key() == action.key[0]:
                        action.moveCursor(self.cursor)
                        self.setTextCursor(self.cursor)

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
