import copy
from random import randint
from tkinter import Canvas, Frame, BOTH, Button
import constants
import colorsys



class View(Frame):
    list_old = []
    width = 0
    height = 0
    savePath = []
    save = dict()

    def __init__(self, parent, products, work, Factory):
        Frame.__init__(self, parent)
        self.saveWorks = work
        self.parent = parent
        self.initUI()
        self.getSize(work)
        self.drawGrid(self.size)
        self.drawWorkstations(work, self.size)
        self.drawProduct(products, self.size)
        self.save_products = products
        self.factory = Factory
        self.button1 = Button(self.parent, text='Reset', command=self.reset)
        self.pathButton = Button(self.parent, text = 'show Path', command=self.showPath)

        #self.button1.pack()
    pathIsVisible = False
    havePathAlready = False
    def showPath(self):
        if constants.SHOW_PRODUCT_PATH == False:
            raise Exception('DRAW EVERY CYCLE IS NOT ACTIVATED')
            return
        if self.pathIsVisible == False:
            self.drawPath()
            self.save.clear()
            self.havePathAlready = True
            self.pathIsVisible = True
            self.pathButton["text"] = "hide Path"
            pass
        else:
            self.drawGrid(self.size)
            self.drawWorkstations(size=self.size, works=self.saveWorks)
            self.pathIsVisible = False
            self.pathButton["text"] = "show Path"
            pass


    def showButton(self):
        self.button1.pack(side = "left")
        if constants.SHOW_PRODUCT_PATH == True:
            self.pathButton.pack(side = "left")

    def reset(self):
        if self.havePathAlready == False:
            self.havePathAlready = True
        if self.pathIsVisible:
            self.showPath()
        self.button1.pack_forget()
        self.pathButton.pack_forget()
        self.factory.productReset()

        self.factory.run()

    def initUI(self):
        self.parent.title("IMAPPS")
        self.parent.lift()
        self.parent.call('wm', 'attributes', '.', '-topmost', True)
        self.parent.after_idle(self.parent.call, 'wm', 'attributes', '.', '-topmost', False)
        self.pack(fill=BOTH, expand=1)
        View.canvas = Canvas(self, bg="#263238")
        View.canvas.pack(fill=BOTH, expand=1)

    def drawGrid(self, size):
        tX = 0
        tY = 0
        for i in range(self.width):
            for j in range(self.height):
                self.canvas.create_rectangle(i*size + tX, j*size+tY, (i*size)+size+tY, (j*size)+size+tY, fill="#37474F", outline="#455A64")

    def getSize(self, works):
        maxX = 0
        maxY = 0
        for w_v in works.values():
            for w in w_v:
                if w.positionX > maxX:
                    maxX = w.positionX
                if w.positionY > maxY:
                    maxY = w.positionY

        self.width = constants.FIELD_SIZE
        self.height = constants.FIELD_SIZE

        if (600.0/self.height) > (1000.0/self.width):
            self.size = 1000.0 / self.width
        else:
            self.size = 600.0 / self.height
                
    def drawWorkstations(self, works, size):
        for w_v in works.values():
            for w in w_v:
                View.canvas.create_rectangle(w.positionX * size, w.positionY * size, w.positionX * size + size, w.positionY * size + size, fill="#B0BEC5", outline="#607D8B")
                View.canvas.create_text((w.positionX * size + (size / 2), w.positionY * size + (size / 2)), text=w.type)
        pass

    allProductList = []
    def drawProduct(self, products, size):
        counter = 1
        View.list_old.clear()
        theOld = []
        for p in products:
            if not p.isDone:
                self.allProductList.append(View.canvas.create_oval(p.positionX * size + 3, p.positionY * size + 3, p.positionX * size - 3 + size, p.positionY * size - 3 + size, outline="white", fill="#3F51B5", width=0))
                self.allProductList.append(View.canvas.create_text((p.positionX * size + (size / 2), p.positionY * size + (size / 2)), text=str(counter), fill="#E8EAF6"))
                counter+=1
            View.list_old.append((p.positionX, p.positionY))
        return theOld

    def updateProducts(self, products, size):
        if constants.SHOW_PRODUCT_PATH and not self.havePathAlready:
            self.savePath.append(list(self.list_old))
        self.drawProduct(products, size)
        pass

    def nextTimeStep(self, listP, listW):
        for p in self.allProductList:
            self.canvas.delete(p)
        self.allProductList.clear()
        self.updateProducts(listP, self.size)

    def drawPath(self):
        for i in range(len(self.savePath)-1):
            for j in range(len(self.savePath[i])):
                xS = self.savePath[i][j][0]*self.size + self.size / 2
                yS = self.savePath[i][j][1]*self.size + self.size / 2
                xE = self.savePath[i+1][j][0] * self.size + self.size / 2
                yE = self.savePath[i+1][j][1] * self.size + self.size / 2

                if (xS, yS) != (xE, yE):
                    if (xS, yS, xE, yE) in self.save:
                         self.save[(xS, yS, xE, yE)] += 0.5
                    else:
                        self.save.update({(xS, yS, xE, yE) : 0.5})


        maxW = max(self.save.values())
        for i in self.save.keys():
            w = self.save[i]
            rgb = colorsys.hsv_to_rgb((120 -((120/maxW) * w))/360,100/100,100/100)
            rgbNew = (round(rgb[0] * 255),round(rgb[1] * 255), round(rgb[2] * 255))
            View.canvas.create_line(i[0], i[1], i[2], i[3],fill= '#%02x%02x%02x' % (rgbNew[0], rgbNew[1], rgbNew[2]), width=w)




