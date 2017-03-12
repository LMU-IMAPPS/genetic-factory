from tkinter import Canvas, Frame, BOTH, Button

import time


class WorkstationView(Frame):
    list_old = []
    width = 0
    height = 0

    def __init__(self, parent, work, width, heigth):
        Frame.__init__(self, parent)
        self.width = width
        self.height = heigth
        self.parent = parent
        self.initUI()
        self.getSize()
        self.drawGrid(self.size)
        self.drawWorkstations(work, self.size)

    def initUI(self):
        self.parent.title("IMAPPS")
        self.parent.lift()
        self.parent.call('wm', 'attributes', '.', '-topmost', True)
        self.parent.after_idle(self.parent.call, 'wm', 'attributes', '.', '-topmost', False)
        self.pack(fill=BOTH, expand=1)
        WorkstationView.canvas = Canvas(self, bg="white")
        WorkstationView.canvas.pack(fill=BOTH, expand=1)

    def drawGrid(self, size):
        tX = 0
        tY = 0
        for i in range(self.width):
            for j in range(self.height):
                self.canvas.create_rectangle(i * size + tX, j * size + tY, (i * size) + size + tY,
                                             (j * size) + size + tY)

    def getSize(self):

        if (600.0 / self.height) > (1000.0 / self.width):
            self.size = 1000.0 / self.width
        else:
            self.size = 600.0 / self.height

            # return size

    def drawWorkstations(self, idv, size):
        for i in idv.DNA:
            WorkstationView.canvas.create_rectangle(i[1] *size, i[2] *size, i[1] *size + size, i[2] *size + size, fill="pink")
            WorkstationView.canvas.create_text((i[1] *size + (size / 2), i[2] *size + (size / 2)), text=i[0])
            self.list_old.append((i[0], i[1], i[2]))
        pass

    def updateWorkstation(self, size, works):
        for i in self.list_old:
            WorkstationView.canvas.create_rectangle(i[1] *size, i[2] *size, i[1] *size + size, i[2] *size + size, fill = "white")
        self.list_old.clear()
        self.drawWorkstations(works, size)

        pass

    def nextTimeStep(self, idv):
        self.updateWorkstation(self.size, idv)
        #print("step")
        #time.sleep(0.1)

