import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout)
import motion, operators, addconstructor
from matheditor import MyFrame, Fraction, SquareRoot, Subscript, MyLineEdit

    
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.createMyMath()

        MyFrame.updateFrames()
    

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)

        
    def createMyMath(self):
        mainMathFrame = MyFrame(self)
        lineEdit = mainMathFrame.findChild(MyLineEdit)
        lineEdit.setText("example")
        innerFrame = mainMathFrame.createFrameMiddle(2, Subscript)
        # otherInnerFrame = innerFrame.numerator.createFrameMiddle(2, Fraction)
        # squareRootFrame = innerFrame.denominator.createFrameMiddle(2, SquareRoot)
        # fractionInsideSquareFrame = squareRootFrame.squareRootArgumentFrame.createFrameMiddle(2, Fraction)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setStyleSheet("background-color:white")
    window.show()
    sys.exit(app.exec())
