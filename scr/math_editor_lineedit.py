from math_editor_graphics_lineedit import MyGraphicsLineEdit

class MyLineEdit:
    def __init__(self, parent):
        self.parent = parent
        self.parent.children.append(self)
        self.scene = self.parent.scene
        self.scene.addLineEdit(self)
        self.graphicsLineEdit = MyGraphicsLineEdit(self.parent.scene.fontSize, self, self.parent.graphicsFrame)
        self.nextLinedit = None
        self.previousLinedit = None
        self.upperLinedit = None
        self.lowerLinedit = None
        self.graphicsLineEdit.updateWidth()
    

    def setGeometry(self, *args, **kwargs):
        self.graphicsLineEdit.setGeometry(*args, **kwargs)

        
    def setStyle(self, *args, **kwargs):
        self.graphicsLineEdit.setStyle(*args, **kwargs)


    @property
    def u(self): return self.graphicsLineEdit.u
    

    @property
    def d(self): return self.graphicsLineEdit.d
    

    @property
    def width(self): return self.graphicsLineEdit.width
    

    @property
    def height(self): return self.graphicsLineEdit.height