from math_editor_scene import scene
from PySide6.QtWidgets import QMainWindow
from math_editor_frame import MyFrame
from math_editor_lineedit import MyLineEdit

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.scene = scene
        self.scene.window = self

        self.createMyMath()


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

