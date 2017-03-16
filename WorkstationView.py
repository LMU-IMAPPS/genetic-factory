from tkinter import Canvas, Frame, BOTH, Button
import constants
import time


class WorkstationView(Frame):
    #list_old = []
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
        WorkstationView.canvas = Canvas(self, bg="#263238")
        WorkstationView.canvas.pack(fill=BOTH, expand=1)

    def drawGrid(self, size):
        tX = 0
        tY = 0
        for i in range(self.width):
            for j in range(self.height):
                self.canvas.create_rectangle(i * size + tX, j * size + tY, (i * size) + size + tY, (j * size) + size + tY, fill="#37474F", outline="#455A64")

    def getSize(self):

        if (600.0 / self.height) > (1000.0 / self.width):
            self.size = 1000.0 / self.width
        else:
            self.size = 600.0 / self.height

            # return size

    saves = []


    def drawWorkstations(self, idv, size):
        saveDraw = []
        for i in idv.DNA:
            ws = WorkstationView.canvas.create_rectangle(i[1] *size, i[2] *size, i[1] *size + size, i[2] *size + size, fill="#B0BEC5", outline="#607D8B")
            #self.canvas.itemconfig(ws, fill='#74838a')
            ts = WorkstationView.canvas.create_text((i[1] *size + (size / 2), i[2] *size + (size / 2)), text=i[0])
            saveDraw.append((ws,ts))
        self.saves.append(saveDraw)
        pass

    def updateWorkstation(self, size, works):
        if constants.FADE:
            if len(self.saves) >= 1:
                for w in self.saves[len(self.saves)-1]:
                    self.canvas.itemconfig(w[0], fill='#5c6b73')
                    self.canvas.itemconfig(w[1], fill='#2c3948')
                pass
            if len(self.saves) == 2:
                toDel = self.saves.pop(0)
                for d in toDel:
                    self.canvas.delete(d[0])
                    self.canvas.delete(d[1])
        else:
            for toDel in self.saves:
                for d in toDel:
                    self.canvas.delete(d[0])
                    self.canvas.delete(d[1])

        self.drawWorkstations(works, size)

        pass

    def nextTimeStep(self, idv):
        self.updateWorkstation(self.size, idv)

