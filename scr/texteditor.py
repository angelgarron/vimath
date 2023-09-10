import sys
from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QWidget, QVBoxLayout,
                               QProxyStyle)
import motion, operators
from base import actions, actionsVisual

class ThickCursorStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QProxyStyle.PM_TextCursorWidth:
            return 8

        return super().pixelMetric(metric, option, widget)
        
class MyTextEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setText("one two three\nfour (five) six seven eight\n(nine ((ten) eleven)) () (())twelve")
        self.setFont("monospace")
        self.setStyle(ThickCursorStyle())
        # normal:0, insert:1, visual:2
        self.mode = 0
        self.storedKeys = []
        self.actions = actions
        self.actionsVisual = actionsVisual

    def keyPressEvent(self, event):
        if event.keyCombination() == Qt.ControlModifier | Qt.Key_C:
            self.enterNormalMode()
            self.storedKeys = []
            return

        if self.mode == 1:
            super().keyPressEvent(event)
            return

        if self.mode == 0:
            actions = self.actions
        else:
            actions = self.actionsVisual

        if event.key() in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]:
            return

        self.storedKeys.append(event.keyCombination())

        for action in actions.values():
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
        self.setStyle(QProxyStyle())

    def enterNormalMode(self):
        self.mode = 0
        self.setStyle(ThickCursorStyle())

    def enterVisualMode(self):
        self.mode = 2
        self.setStyle(ThickCursorStyle())
    
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
