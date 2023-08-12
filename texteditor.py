import sys
from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout)
import motion, operators
from base import KeyCombination, actions

class MyTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.cursor = self.textCursor()
        self.cursor.insertText("one two three\nfour five six")
        self.setFont("monospace")
        self.setCursorWidth(8)
        # normal:0, insert:1, visual:2
        self.mode = 0
        self.storedKeys = []
        self.actions = actions

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.exitInsertMode()
            self.storedKeys = []
        else:
            if self.mode == 1:
                super().keyPressEvent(event)
            else:
                if event.key() not in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]:
                    if event.modifiers() == Qt.NoModifier:
                        self.storedKeys.append(event.key())
                    else:
                        self.storedKeys.append(KeyCombination(event.modifiers(), event.key()))
                    for action in self.actions.values():
                        if isinstance(action.key[0], list):
                            for key in action.key:
                                if key == self.storedKeys:
                                    action.performAction(self)
                                    self.storedKeys = []
                                    break
                        else:
                            if action.key == self.storedKeys:
                                action.performAction(self)
                                self.storedKeys = []
                                break

    def enterInsertMode(self):
        self.mode = 1
        self.setCursorWidth(1)

    def exitInsertMode(self):
        self.mode = 0
        self.setCursorWidth(8)

    def enterVisualMode(self):
        self.mode = 2
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
