from scene import scene
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel
from frame import MyFrame
from lineedit import MyLineEdit
from constructors import Fraction, MainFrame

MODE_NAME = {
    0: "NORMAL",
    1: "INSERT",
    2: "VISUAL",
}

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.scene = scene
        self.scene.window = self
        self.tp = SelectionRectangle(self)
        self.fontSize = self.scene.fontSize

        self.mainMathFrame = MainFrame(self)
        self.scene.history.store("first stamp")
        self.createMyMath()
        self.modeInfoLabel = QLabel("")
        self.statusBar().addWidget(self.modeInfoLabel, 1)
        self.storedKeysLabel = QLabel("")
        self.statusBar().addWidget(self.storedKeysLabel)
        self.updateStatusBar()


    def updateStatusBar(self):
        modeInfo = f"--{MODE_NAME[self.scene.mode]}--"
        storedKeys = "".join(map(lambda k: str(k.key())[-1].lower(), self.scene.storedKeys))
        self.storedKeysLabel.setText(storedKeys)
        self.modeInfoLabel.setText(modeInfo)

    
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)

        
    def createMyMath(self):
        mainMathFrame = MyFrame(self)
        # lineEdit = mainMathFrame.graphicsFrame.findChild(MyGraphicsLineEdit)
        # lineEdit.setText("example")
        # innerFrame = mainMathFrame.createFrameMiddle(2, Fraction)
        # otherInnerFrame = innerFrame.numerator.createFrameMiddle(2, Fraction)
        # squareRootFrame = innerFrame.denominator.createFrameMiddle(2, SquareRoot)
        # fractionInsideSquareFrame = squareRootFrame.squareRootArgumentFrame.createFrameMiddle(2, Fraction)
        # fractionInsideSquareFrame.numerator.createFrameMiddle(2, Subscript)


class SelectionRectangle(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.hide()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 255, 128))
