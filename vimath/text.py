import re


class Text:
    def __init__(self, text=""):
        self.plain_text = text
        self._cursorPosition = 0

        
    def setText(self, text):
        self.plain_text = text


    def splitText(self):
        split_text = []
        for sp in re.findall(r"(\d+|\D+)", self.plain_text):
            s = "\\"
            splitis = re.split(f"(?={re.escape(s)})", sp)
            for ss in splitis:
                for aa in ss.split(" "):
                    if aa == "":
                        continue
                    split_text.append(aa)
        return split_text

        
    def __len__(self):
        return len(self.furtherSplitting())


    def text(self):
        return self.plain_text

    
    def furtherSplitting(self):
        furtherSplit = []
        for sub in self.splitText():
            if sub[0] == "\\":
                furtherSplit.append(sub)
            else:
                for subb in sub:
                    furtherSplit.append(subb)
        return furtherSplit

        
    def __getitem__(self, index):
        further_splitted = self.furtherSplitting()[index]
        joined = []
        for sub in further_splitted:
            if sub[0] != "\\":
                joined.append(sub)
            else:
                joined.append(sub+" ")
        joined =  "".join(joined)
        if joined and joined[-1] == " ": # check that string is not empty, remove whitespace at the end
            joined = joined[:len(joined)-1]
        return Text(joined)

        
    def cursorPosition(self):
        return self._cursorPosition
    

    def setCursorPosition(self, position):
        self._cursorPosition = position

        
    def cursorForward(self):
        if self._cursorPosition == len(self):
            return
        self._cursorPosition += 1
    

    def cursorBackward(self):
        if self._cursorPosition == 0:
            return
        self._cursorPosition -= 1

        
    def setText(self, text):
        if isinstance(text, str):
            self.plain_text = text
        elif isinstance(text, Text):
            self.plain_text = text.plain_text


    def insertTextOnCursorPosition(self, text):
        if text[0] == "\\": # adding whitespace at the end of math symbols
            text += " "
        self.plain_text = self[:self._cursorPosition].plain_text+text+self[self._cursorPosition:].plain_text
        if self.plain_text[-1] == " ": # remove whitespace at the end
            self.plain_text = self.plain_text[:len(self.plain_text)-1]
        self.cursorForward()

        
    def backspace(self):
        self.plain_text = self.plain_text[:self._cursorPosition-1]+self.plain_text[self._cursorPosition:]
        self.cursorBackward()

        
    def home(self):
        self._cursorPosition = 0
    

    def end(self):
        self._cursorPosition = len(self)


    def __add__(self, other):
        return Text(self.plain_text+other.plain_text)

        
    def clear(self):
        self.plain_text = ""
