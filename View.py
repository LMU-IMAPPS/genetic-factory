import copy
from tkinter import Canvas, Frame, BOTH, Button



class View(Frame):
    list_old = []
    width = 0
    height = 0
    savePath = []

    def __init__(self, parent, products, work, Factory):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.getSize(work)
        self.drawGrid(self.size)
        self.drawWorkstations(work, self.size)
        self.drawProduct(products, self.size)
        self.save_products = products
        self.factory = Factory
        self.button1 = Button(self.parent, text='Reset', command=self.reset)
        #self.button1.pack()

    def showButton(self):
        self.button1.pack()

    def reset(self):
        self.button1.pack_forget()
        self.factory.productReset()
        self.factory.run()

    def initUI(self):
        self.parent.title("IMAPPS")
        self.parent.lift()
        self.parent.call('wm', 'attributes', '.', '-topmost', True)
        self.parent.after_idle(self.parent.call, 'wm', 'attributes', '.', '-topmost', False)
        self.pack(fill=BOTH, expand=1)
        View.canvas = Canvas(self, bg="white")
        View.canvas.pack(fill=BOTH, expand=1)

    def drawGrid(self, size):
        tX = 0
        tY = 0
        for i in range(self.width):
            for j in range(self.height):
                self.canvas.create_rectangle(i*size + tX, j*size+tY, (i*size)+size+tY, (j*size)+size+tY)

    def getSize(self, works):


        #size = 0
        maxX = 0
        maxY = 0
        for w_v in works.values():
            for w in w_v:
                if w.positionX > maxX:
                    maxX = w.positionX
                if w.positionY > maxY:
                    maxY = w.positionY

        self.width = maxX+1
        self.height = maxY+1

        if (600.0/self.height) > (1000.0/self.width):
            self.size = 1000.0 / self.width
        else:
            self.size = 600.0 / self.height

        #return size
                
    def drawWorkstations(self, works, size):
        for w_v in works.values():
            for w in w_v:
                View.canvas.create_rectangle(w.positionX * size, w.positionY * size, w.positionX * size + size, w.positionY * size + size, fill="pink")
                View.canvas.create_text((w.positionX * size + (size / 2), w.positionY * size + (size / 2)), text=w.type)
        pass

    def drawProduct(self, products, size):
        counter = 1
        View.list_old.clear()
        for p in products:
            if not p.isDone:
                View.canvas.create_oval(p.positionX * size + 3, p.positionY * size + 3, p.positionX * size - 3 + size, p.positionY * size - 3 + size, outline="white", fill="blue", width=0)
                View.canvas.create_text((p.positionX * size + (size / 2), p.positionY * size + (size / 2)), text=str(counter), fill="white")
                counter+=1
            View.list_old.append((p.positionX, p.positionY))
        pass

    def updateProducts(self, products, size, works):
        self.savePath.append(copy.deepcopy( self.list_old))
        #print(self.savePath)
        for p in View.list_old:
            View.canvas.create_oval(p[0] * size + 1, p[1] * size + 1, p[0] * size - 1 + size, p[1] * size - 1 + size, outline="gray", fill="white", width=0)
        self.drawWorkstations(works, size)
        self.drawProduct(products, size)

        pass

    def nextTimeStep(self, listP, listW):
        #size = self.getSize(listW)
        self.updateProducts(listP, self.size, listW)

    def drawPath(self):

        for i in range(len(self.savePath)-1):
            for j in range(len(self.savePath[i])):
                View.canvas.create_line(self.savePath[i][j][0]*self.size + self.size / 2,
                                        self.savePath[i][j][1]*self.size + self.size / 2,
                                        self.savePath[i+1][j][0] * self.size + self.size / 2,
                                        self.savePath[i+1][j][1] * self.size + self.size / 2,
                                        fill="blue", dash = (10,100), width=2)





