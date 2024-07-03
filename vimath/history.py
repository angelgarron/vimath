class History():
    def __init__(self, scene):
        self.scene = scene

        self.stack = []
        self.currentStep = -1
        self.limit = 10


    def undo(self):
        if self.currentStep > 0:
            self.currentStep -= 1
            self.restore()


    def redo(self):
        if self.currentStep+1 < len(self.stack):
            self.currentStep += 1
            self.restore()


    def restore(self):
        self.restoreStamp(self.stack[self.currentStep])


    def store(self, description):
        if self.currentStep+1 < len(self.stack):
            self.stack = self.stack[0:self.currentStep+1]

        if self.currentStep+1 >= self.limit:
            self.stack = self.stack[1:]
            self.currentStep -= 1

        hs = self.createStamp(description)

        self.stack.append(hs)
        self.currentStep += 1


    def createStamp(self, description):
        stamp = {
            "description": description,
            "snapshot": self.scene.serialize(),
        }
        return stamp


    def restoreStamp(self, stamp):
        self.scene.deserialize(stamp["snapshot"])
