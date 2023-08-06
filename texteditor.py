import sys
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QKeySequence, QShortcut, QTextCursor)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget)

movements = {
    "h":QTextCursor.MoveOperation.PreviousCharacter, 
    "j":QTextCursor.MoveOperation.Down, 
    "k":QTextCursor.MoveOperation.Up, 
    "l":QTextCursor.MoveOperation.NextCharacter, 
    "b":QTextCursor.MoveOperation.PreviousWord, 
    "w":QTextCursor.MoveOperation.NextWord, 
    "e":[QTextCursor.MoveOperation.NextWord, 
         QTextCursor.MoveOperation.EndOfWord, 
         QTextCursor.MoveOperation.PreviousCharacter], 
    }


class MyTextEdit(QTextEdit):
    def __init__(self, widget):
        super().__init__(widget)
        self.cursor = self.textCursor()
        self.cursor.insertText("hola como va\n todo por ahí")
        self.setFont("monospace")
        self.setCursorWidth(8)
        self.insert_mode = False

    def keyPressEvent(self, event):
        if event.text() == "i":
            self.insert_mode = True
        elif not self.insert_mode:
            if event.text() in movements.keys():
                self.moveCursor(event.text())
            else:
                pass
        else:
            super().keyPressEvent(event)

    def moveCursor(self, char):
        movement = movements[char]
        if isinstance(movement, list):
            for m in movement:
                self.cursor.movePosition(m, self.cursor.MoveMode.MoveAnchor, 1)
                self.setTextCursor(self.cursor)
        else:
            self.cursor.movePosition(movement, self.cursor.MoveMode.MoveAnchor, 1)
            self.setTextCursor(self.cursor)
            

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(658, 427)
        self.centralwidget = QWidget(MainWindow)
        self.textEdit = MyTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QRect(80, 40, 501, 311))
        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())
