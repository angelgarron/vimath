from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont
from PySide6.QtCore import Qt, QSize

LINEDIT_SIZE = (8, 20)


class ThickCursorStyle(QProxyStyle):
    def __init__(self, fontSize):
        super().__init__()
        self.fontSize = fontSize
    

    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QProxyStyle.PM_TextCursorWidth:
            return self.fontSize

        return super().pixelMetric(metric, option, widget)


class EmptyCursorStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QProxyStyle.PM_TextCursorWidth:
            return 0

        return super().pixelMetric(metric, option, widget)


class MyLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.fontSize = self.parent.fontSize
        self.isEmpty = False
        self.thickCursorStyle = ThickCursorStyle(self.fontSize)
        self.thinCursorStyle = QProxyStyle()
        self.emptyCursorStyle = EmptyCursorStyle()
        self.setThickCursorStyle()
        self.setFont(QFont("monospace", self.fontSize))
        self.scene = self.parent.scene
        self.scene.addLineEdit(self)
        self.u = self.parent.fontSize/2+2
        self.d = self.parent.fontSize/2+2
        self.setGeometry(0, 0, LINEDIT_SIZE[0], self.u+self.d)
        self.textChanged.connect(self.scene.updateFrames)
        self.textEdited.connect(self.wasEdited)
        self.cursorPositionChanged.connect(self.scene.window.graphicCursor.updatePosition)
        self.pen = QPen()
        self.color_blue = QColor(36, 143, 230)
        self.color_blue_dark = QColor(30, 112, 180)
        self.pen.setColor(self.color_blue_dark)
        self.pen.setStyle(Qt.DashLine)
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.show()
    

    def inputMethodEvent(self, event):
        if event.commitString() == "^":
            self.scene.actions["CreateSuperscript"].performAction(self)
            return
        return super().inputMethodEvent(event)


    def setThickCursorStyle(self):
        if not self.isEmpty:
            self.setStyle(self.thickCursorStyle)
    

    def setThinCursorStyle(self):
        if not self.isEmpty:
            self.setStyle(self.thinCursorStyle)
    

    def setEmpty(self, flag):
        if flag:
            self.setStyle(self.emptyCursorStyle)
            self.isEmpty = True
        else:
            self.isEmpty = False
            if self.scene.isInsertMode():
                self.setThinCursorStyle()
            elif self.scene.isNormalMode() or self.scene.isVisualMode():
                self.setThickCursorStyle()
                
        
    @property
    def nextLinedit(self):
        indx = self.parent.children.index(self)+1
        try:
            return self.parent.children[indx].firstLinedit
        except IndexError: # we were in the last element of the frame
            return self.parent.nextLinedit
    

    @property
    def previousLinedit(self):
        indx = self.parent.children.index(self)-1
        if indx == -1: # we were in the first element of the frame
            return self.parent.previousLinedit
        return self.parent.children[indx].lastLinedit
        
        
    @property
    def upperLinedit(self):
        return self.parent.upperLinedit
    

    @property
    def lowerLinedit(self):
        return self.parent.lowerLinedit
        
        
    def wasEdited(self):
        text = self.text()
        for action in self.scene.actionsInsert.values():
            cursorPosition = text.find(action.key[0])
            if cursorPosition != -1:
                action.performAction(self, cursorPosition, text)


    def updateWidth(self):
        if len(self.text()) == 0: # how to display empty lineEdit
            if len(self.parent.children) == 1:
                self.setFixedWidth(self.parent.fontSize)
                self.setFixedHeight(self.parent.fontSize*1.2)
                self.setEmpty(True)
            else:
                self.setFixedWidth(4)
                self.setFixedHeight(self.parent.fontSize*1.2)
                self.setEmpty(False)
        else:
            self.setEmpty(False)
            width = self.fontMetrics().horizontalAdvance(self.text())
            self.setFixedWidth(width+8)
            tight = self.fontMetrics().tightBoundingRect(self.text())
            self.setFixedHeight(tight.height()+6)
            self.setTextMargins(0, -tight.top()-self.font().pointSize()-2, 0, 0)
            self.u = -tight.top()
            self.d = self.height()-self.u
            self.setGeometry(self.x(), self.y(), self.width(), self.u+self.d)


    def createFrameMiddle(self, FrameConstructor, storeHistory=True):
        cursorPosition = self.cursorPosition()
        newFrame = FrameConstructor(self.parent)
        newFrame.setFirstLineEdit()
        currentLineditPosition = self.parent.children.index(self)
        self.parent.children.insert(currentLineditPosition+1, newFrame)
        rightLineEdit = MyLineEdit(self.parent)
        self.parent.children.insert(currentLineditPosition+2, rightLineEdit)
        rightLineEdit.setText(self.text()[cursorPosition:])
        self.setText(self.text()[:cursorPosition])
        newFrame.firstLinedit.setFocus()
        self.scene.updateFrames()
        if storeHistory:
            self.scene.history.store(f"create frame {FrameConstructor}")
        return newFrame
        

    def deleteText(self):
        if self.hasSelectedText():
            self.del_()


    def keyPressEvent(self, event):
        if event.keyCombination() == Qt.ControlModifier | Qt.Key_C:
            self.scene.storedKeys = []
            self.scene.window.updateStatusBar()
            if not self.scene.isNormalMode():
                self.cursorBackward(False)
                self.scene.enterNormalMode()
                self.scene.history.store("enter normal mode from insert mode")
            return

        if self.scene.isInsertMode():
            super().keyPressEvent(event)
            return

        if self.scene.isNormalMode():
            actions = self.scene.actions
        else:
            actions = self.scene.actionsVisual

        if event.key() in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]:
            return

        self.scene.storedKeys.append(event.keyCombination())
        self.scene.window.updateStatusBar()

        for action in actions.values():
            if isinstance(action.key[0], list):
                for key in action.key:
                    if key == self.scene.storedKeys:
                        action.performAction(self)
                        self.scene.storedKeys = []
                        self.scene.window.updateStatusBar()
                        if self.scene.isVisualMode():
                            self.scene.updateVisualSelection()
                        break
            else:
                if action.key == self.scene.storedKeys:
                    action.performAction(self)
                    self.scene.storedKeys = []
                    self.scene.window.updateStatusBar()
                    if self.scene.isVisualMode():
                        self.scene.updateVisualSelection()
                    break


    def serialize(self, start=None, end=None):
        return {
            "constructor": str(self.__class__),
            "text": self.text()[start:end],
        }

        
    def deserialize(self, data):
        return
        

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isEmpty:
            with QPainter(self) as painter:
                if self.hasFocus():
                    self.brush.setColor(self.color_blue_dark.darker())
                else:
                    self.brush.setColor(self.color_blue)
                rect = self.contentsRect()
                rect.setHeight(rect.height()-2.5)
                rect.setWidth(rect.width()-2.5)
                rect.setX(rect.x()+2.5)
                rect.setY(rect.y()+2.5)
                painter.setPen(self.pen)
                painter.setBrush(self.brush)
                painter.drawRect(rect)
        