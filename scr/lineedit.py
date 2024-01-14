import re
from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont, QTextLayout, QFontMetrics
from PySide6.QtCore import Qt, QSize, QPoint

LINEDIT_SIZE = (8, 20)


class EmptyCursorStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QProxyStyle.PM_TextCursorWidth:
            return 0

        return super().pixelMetric(metric, option, widget)


class MyLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.fontSize = self.parent.fontSize
        self.isEmpty = False
        # hiding cursor to just see my implementation
        self.setStyle(EmptyCursorStyle())
        self.fontItalics = QFont("cmmi10", self.fontSize)
        self.fontPlain = QFont("cmr10", self.fontSize)
        self.fmItalics = QFontMetrics(self.fontItalics)
        self.fmPlain = QFontMetrics(self.fontPlain)
        self.scene = self.parent.scene
        self.u = self.parent.fontSize/2+2
        self.d = self.parent.fontSize/2+2
        self.setGeometry(0, 0, LINEDIT_SIZE[0], self.u+self.d)
        self.textChanged.connect(self.scene.updateFrames)
        self.cursorPositionChanged.connect(self.scene.window.graphicCursor.updatePosition)
        self.pen = QPen()
        self.color_blue = QColor(36, 143, 230)
        self.color_blue_dark = QColor(30, 112, 180)
        self.pen.setColor(self.color_blue_dark)
        self.pen.setStyle(Qt.DashLine)
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.show()
    

    def focusInEvent(self, event):
        self.scene.window.graphicCursor.updatePosition()
        self.parent.setProperty("showBox", "true")
        self.parent.style().unpolish(self.parent)
        self.parent.style().polish(self.parent)
        return super().focusInEvent(event)
    

    def focusOutEvent(self, event):
        self.parent.setProperty("showBox", "false")
        self.parent.style().unpolish(self.parent)
        self.parent.style().polish(self.parent)
        return super().focusOutEvent(event)



    def inputMethodEvent(self, event):
        if event.commitString() == "^":
            self.scene.actions["CreateSuperscript"].performAction(self)
            return
        return super().inputMethodEvent(event)


    def setEmpty(self, flag):
        if flag:
            self.isEmpty = True
        else:
            self.isEmpty = False
                
        
    @property
    def nextLineEdit(self):
        indx = self.parent.children.index(self)+1
        try:
            return self.parent.children[indx].firstLineEdit
        except IndexError: # we were in the last element of the frame
            return self.parent.nextLineEdit
    

    @property
    def previousLineEdit(self):
        indx = self.parent.children.index(self)-1
        if indx == -1: # we were in the first element of the frame
            return self.parent.previousLineEdit
        return self.parent.children[indx].lastLineEdit
        
        
    @property
    def upperLineEdit(self):
        return self.parent.upperLineEdit
    

    @property
    def lowerLineEdit(self):
        return self.parent.lowerLineEdit
        
        

    def getWidthUntilCursorPosition(self, cursorPosition):
        result_list = re.findall(r'[a-zA-Z]+|[^a-zA-Z]+', self.text()[:cursorPosition])
        if len(result_list) > 0:
            isItalic = result_list[0].isalpha()
        else:
            isItalic = False

        self.u = 0
        self.d = 0
        width = 0
        for group in result_list:

            if isItalic:
                fm = self.fmItalics
            else:
                fm = self.fmPlain

            tight = fm.tightBoundingRect(group)

            u = -tight.top()
            d = tight.height()-u
            self.u = max(self.u, u)
            self.d = max(self.d, d)
            width += tight.width()

            isItalic = not isItalic

        self.setFixedHeight(self.u+self.d)
        return width

    
    def updateWidth(self):
        if len(self.text()) == 0: # how to display empty lineEdit
            if len(self.parent.children) == 1:
                self.setFixedWidth(self.parent.fontSize)
                self.setFixedHeight(self.parent.fontSize*1.2)
                self.setEmpty(True)
            else:
                self.setFixedWidth(0)
                self.setFixedHeight(self.parent.fontSize*1.2)
                self.setEmpty(False)
        else:
            self.setEmpty(False)
            width = self.getWidthUntilCursorPosition(None)
            self.setFixedWidth(width)
            # self.setFixedHeight(height)
            # self.u = self.height()/2
            # self.d = self.height()-self.u


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
        newFrame.firstLineEdit.setFocus()
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

        if event.key() in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]:
            return

        if self.scene.isInsertMode():
            actions = self.scene.actionsInsert
        elif self.scene.isNormalMode():
            actions = self.scene.actions
        else:
            actions = self.scene.actionsVisual

        self.scene.storedKeys.append(event.keyCombination())

        isPossibleMatch = False
        for action in actions.values():
            if isinstance(action.key[0], list):
                for key in action.key:
                    isPossibleMatch = isPossibleMatch or self.isPossibleMatch(key)
                    if key == self.scene.storedKeys:
                        action.performAction(self)
                        self.scene.storedKeys = []
                        if self.scene.isVisualMode():
                            self.scene.updateVisualSelection()
                        break
                else:
                    continue
                break
            else:
                isPossibleMatch = isPossibleMatch or self.isPossibleMatch(action.key)
                if action.key == self.scene.storedKeys:
                    action.performAction(self)
                    self.scene.storedKeys = []
                    if self.scene.isVisualMode():
                        self.scene.updateVisualSelection()
                    break

        if not isPossibleMatch:
            self.scene.storedKeys = []
            if self.scene.isInsertMode():
                super().keyPressEvent(event)

        self.scene.window.updateStatusBar()

    
    def isPossibleMatch(self, keys):
        for key, storedKey in zip(keys, self.scene.storedKeys):
            if key != storedKey:
                return False
        return True



    def getAbsolutePosition(self, element, pos):
        pos += element.pos()
        if element.parent == self.scene.window:
            return pos
        return self.getAbsolutePosition(element.parent, pos)


    @property
    def geometryCursorPosition(self):
        cursorPosition = self.cursorPosition()
        start = self.x()+\
            self.getWidthUntilCursorPosition(cursorPosition)
        pos = self.getAbsolutePosition(self.parent, QPoint(start, self.y()))
        return pos

        
    def serialize(self, start=None, end=None):
        return {
            "constructor": str(self.__class__),
            "text": self.text()[start:end],
        }

        
    def deserialize(self, data):
        return
        

    def paintEvent(self, event):
        with QPainter(self) as painter:
            result_list = re.findall(r'[a-zA-Z]+|[^a-zA-Z]+', self.text())
            if len(result_list) > 0:
                isItalic = result_list[0].isalpha()
            else:
                isItalic = False

            u = 0
            d = 0
            for group in result_list:

                if isItalic:
                    font = self.fontItalics
                    fm = self.fmItalics
                else:
                    font = self.fontPlain
                    fm = self.fmPlain

                tight = fm.tightBoundingRect(group)

                newu = -tight.top()
                newd = tight.height()-newu
                u = max(u, newu)
                d = max(d, newd)

                isItalic = not isItalic


            if len(result_list) > 0:
                isItalic = result_list[0].isalpha()
            else:
                isItalic = False

            width = 0
            for group in result_list:

                if isItalic:
                    font = self.fontItalics
                    fm = self.fmItalics
                else:
                    font = self.fontPlain
                    fm = self.fmPlain

                tight = fm.tightBoundingRect(group)

                l = QTextLayout(group, font)
                l.beginLayout()
                l.createLine()
                l.endLayout()
                l.draw(painter, QPoint(
                    width
                    -fm.leftBearing(group[0]),
                    -fm.ascent()+u
                ))

                width += tight.width()

                isItalic = not isItalic

    
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
        