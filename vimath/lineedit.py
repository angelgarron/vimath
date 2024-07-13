import re
from PySide6.QtWidgets import (QLineEdit, QFrame, QProxyStyle)
from PySide6.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QFont, QTextLayout, QFontMetrics
from PySide6.QtCore import Qt, QSize, QPoint
from vimath.utils import symbols
from vimath.text import Text
from vimath.utils import translateUnicode

LINEDIT_SIZE = (8, 20)


class MyLineEdit(QLineEdit):
    MIDDLE_GAP = 6
    def __init__(self, parent):
        super().__init__(parent)
        self._text = Text()
        self.parent = parent
        self.fontSize = self.parent.fontSize
        self.isEmpty = False
        # hiding cursor to just see my implementation
        self.fontDict = {
            "cmmi10": QFont("cmmi10", self.fontSize),
            "cmr10": QFont("cmr10", self.fontSize),
            "cmsy10": QFont("cmsy10", self.fontSize),
            "cmex10": QFont("cmex10", self.fontSize),
                                }
        self.fontMetricsDict = {
            "cmmi10": QFontMetrics(self.fontDict["cmmi10"]),
            "cmr10": QFontMetrics(self.fontDict["cmr10"]),
            "cmsy10": QFontMetrics(self.fontDict["cmsy10"]),
            "cmex10": QFontMetrics(self.fontDict["cmex10"]),
                                }
        self.scene = self.parent.scene
        self.u = self.parent.fontSize/2+2
        self.d = self.parent.fontSize/2+2
        self.setGeometry(0, 0, LINEDIT_SIZE[0], self.u+self.d)
        self.pen = QPen()
        self.color_blue = QColor(36, 143, 230)
        self.color_blue_dark = QColor(30, 112, 180)
        self.pen.setColor(self.color_blue_dark)
        self.pen.setStyle(Qt.DashLine)
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.show()
    

    def text(self):
        return self._text

        
    def setText(self, text):
        self._text.setText(text)
        self.scene.updateFrames()


    def cursorPosition(self):
        return self._text.cursorPosition()

        
    def setCursorPosition(self, position):
        return self._text.setCursorPosition(position)

        
    def cursorForward(self, mark, steps=1):
        self._text.cursorForward(mark, steps)
        self.scene.window.graphicCursor.updatePosition()
    

    def cursorBackward(self, mark, steps=1):
        self._text.cursorBackward(mark, steps)
        self.scene.window.graphicCursor.updatePosition()

        
    def home(self, mark):
        self._text.home()


    def end(self, mark):
        self._text.end()

        
    def backspace(self):
        self._text.backspace()
        self.scene.updateFrames()

        
    def clear(self):
        self._text.clear()
        self.scene.updateFrames()


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
        

    def groupCharacters(self, cursorPosition):
        """Group string according to the font each group should display.

        Args:
            cursorPosition (Int): Length of text to consider.

        Returns:
            List: List of tuples [(fontName, group), ...]
        """
        result_list = self._text[:cursorPosition].splitText()
        groups = []
        for group in result_list:
            if group[0].isalpha():
                groups.append(("cmmi10", group))
            elif group[0] == "\\":
                fontAndUnicode = translateUnicode[group]
                groups.append((fontAndUnicode[0], fontAndUnicode[1]))
            else:
                groups.append(("cmr10", group))
        return groups


    def getDimensionUntilCursorPosition(self, cursorPosition):
        groups = self.groupCharacters(cursorPosition)

        u = 0
        d = 0
        width = 0
        for fontName, group in groups:

            fm = self.fontMetricsDict[fontName]

            tight = fm.tightBoundingRect(group)

            newu = -tight.top()
            newd = tight.height()-newu
            u = max(u, newu)
            d = max(d, newd)
            width += tight.width()

        return width, u, d

    
    def updateWidth(self):
        # how to display empty frame
        if len(self.text()) == 0: 
            if len(self.parent.children) == 1:
                self.setFixedWidth(self.parent.fontSize)
                self.setFixedHeight(self.parent.fontSize*1.2)
                u = self.height()
                self.isEmpty = True
            else: # there are more elements in the frame, so it's not empty
                self.setFixedWidth(0)
                self.setFixedHeight(0)
                u = 0
                self.isEmpty = False
        else:
            self.isEmpty = False
            width, u, d = self.getDimensionUntilCursorPosition(None)
            self.setFixedHeight(u+d)
            self.setFixedWidth(width)

        self.u = u-MyLineEdit.MIDDLE_GAP
        self.d = self.height()-self.u


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
        if self.text().indicesSelectedText:
            self.text().del_()
            self.scene.updateFrames()


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
                self._text.insertTextOnCursorPosition(event.text())
                self.scene.updateFrames()

        self.scene.window.updateStatusBar()

    
    def isPossibleMatch(self, keys):
        for key, storedKey in zip(keys, self.scene.storedKeys):
            if key != storedKey:
                return False
        return True


    def getAbsolutePosition(self, element, pos):
        """Transform the coordinates from the element frame
        to the absolute frame
        """
        pos += element.pos()
        if element.parent == self.scene.window:
            return pos
        return self.getAbsolutePosition(element.parent, pos)


    @property
    def geometryCursorPosition(self):
        cursorPosition = self.cursorPosition()
        width, _, _ = self.getDimensionUntilCursorPosition(cursorPosition)
        pos = self.getAbsolutePosition(self, QPoint(width, self.u-self.fontSize*0.8))
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
            groups = self.groupCharacters(None)

            width = 0
            for fontName, group in groups:

                fm = self.fontMetricsDict[fontName]
                font = self.fontDict[fontName]

                tight = fm.tightBoundingRect(group)

                l = QTextLayout(group, font)
                l.beginLayout()
                l.createLine()
                l.endLayout()
                l.draw(painter, QPoint(
                    -fm.leftBearing(group[0])+width,
                    -fm.ascent()+self.u+MyLineEdit.MIDDLE_GAP
                ))

                width += tight.width()

    
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
        