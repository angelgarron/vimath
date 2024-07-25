from vimath.scene import scene
from PySide6.QtWidgets import QMainWindow, QLabel
from vimath.constructors import Fraction, MainFrame
from vimath.graphicalcursor import GraphicalCursor
from vimath.selectionrectangle import SelectionRectangle


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.scene = scene
        self.scene.window = self
        self.selectionRectangle = SelectionRectangle(self)
        self.graphicCursor = GraphicalCursor(self, self.scene)
        self.fontSize = self.scene.fontSize

        # doing updateFrame when creating MainFrame, 
        # but that needs existing mainMathFrame,
        # so I am separating the creation from the initialization
        self.mainMathFrame = MainFrame.__new__(MainFrame)
        self.mainMathFrame.__init__(self)

        self.scene.history.store("first stamp")
        self.createMyMath()
        self.modeInfoLabel = QLabel("")
        self.statusBar().addWidget(self.modeInfoLabel, 1)
        self.storedKeysLabel = QLabel("")
        self.statusBar().addWidget(self.storedKeysLabel)
        self.updateStatusBar()
        self.graphicCursor.updatePosition()


    def updateStatusBar(self):
        modeInfo = f"-- {self.scene.currentMode} --"
        storedKeys = "".join(map(lambda k: str(k.key())[-1].lower(), self.scene.storedKeys))
        self.storedKeysLabel.setText(storedKeys)
        self.modeInfoLabel.setText(modeInfo)

    
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)

        
    def createMyMath(self):
        lineEdit = self.mainMathFrame.children[0].firstLineEdit
        # lineEdit.setText("example")
        lineEdit.setCursorPosition(3)
        innerFrame = lineEdit.createFrameMiddle(Fraction)
        # innerFrame.removeFrame()
        # otherInnerFrame = innerFrame.numerator.createFrameMiddle(2, Fraction)
        # squareRootFrame = innerFrame.denominator.createFrameMiddle(2, SquareRoot)
        # fractionInsideSquareFrame = squareRootFrame.squareRootArgumentFrame.createFrameMiddle(2, Fraction)
        # fractionInsideSquareFrame.numerator.createFrameMiddle(2, Subscript)

        self.scene.updateFrames()
