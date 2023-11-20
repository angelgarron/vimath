import motion, operators, addconstructor
from math_editor_scene import Scene
from PySide6.QtWidgets import QMainWindow
from matheditor import MyFrame, Fraction, SquareRoot, Subscript
from math_editor_graphics_lineedit import MyGraphicsLineEdit

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.fontSize = 15
        self.initUI()
        self.scene = Scene()

        self.createMyMath()


    def initUI(self):
        self.setGeometry(100, 100, 400, 300)

        
    def createMyMath(self):
        mainMathFrame = MyFrame(self)
        lineEdit = mainMathFrame.findChild(MyGraphicsLineEdit)
        lineEdit.setText("example")
        # innerFrame = mainMathFrame.createFrameMiddle(2, Fraction)
        # otherInnerFrame = innerFrame.numerator.createFrameMiddle(2, Fraction)
        # squareRootFrame = innerFrame.denominator.createFrameMiddle(2, SquareRoot)
        # fractionInsideSquareFrame = squareRootFrame.squareRootArgumentFrame.createFrameMiddle(2, Fraction)
        # fractionInsideSquareFrame.numerator.createFrameMiddle(2, Subscript)

