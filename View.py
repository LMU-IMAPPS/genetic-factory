from tkinter import Tk, Canvas, Frame, BOTH
from Workstation import Workstation
from random import randint
from Product import Product

class View(Frame):
    list_old = []

    def __init__(self, parent, products, work):
        Frame.__init__(self, parent)
        canvas = None
        self.parent = parent
        
        self.initUI()
        size = self.getSize(work)
        self.drawGrid(size)
        self.drawWorkstations(work, size)
        self.drawProduct(products, size)
        
    def initUI(self):
      
        self.parent.title("IMAPS")        
        self.pack(fill=BOTH, expand=1)
    
        View.canvas = Canvas(self,bg ="white")
        View.canvas.pack(fill=BOTH, expand=1)
        
    def drawGrid(self, size):
        tX = 0
        tY = 0
        for i in range(round(600/size)):
            for j in range(round(1000/size)):
                self.canvas.create_rectangle(i*size + tX, j*size+tY, (i*size)+size+tY, (j*size)+size+tY)
                
    def getSize(self, works):
        size = 0
        minX = 10000
        maxX = 0
        minY = 10000
        maxY = 0
        print(works.values())
        for w_v in works.values():
            for w in w_v:
                if w.positionX < minX:
                    minX = w.positionX
                if w.positionX > maxX:
                    maxX = w.positionX
                if w.positionY < minY:
                    minY = w.positionY
                if w.positionY > maxY:
                    maxY = w.positionY
                
        if(1000.0/(1+(maxX-minX)) > 600.0/(1+(maxY-minY))):
            size = 600.0/(1+(maxY-minY))
        else:
            size = 1000.0/(1+(maxX-minX))
        
        return size   
                
    def drawWorkstations(self, works, size):
        for w_v in works.values():
            for w in w_v:
                View.canvas.create_rectangle(w.positionX*size , w.positionY*size, w.positionX*size+size,w.positionY*size+size, fill="pink")
                View.canvas.create_text((w.positionX*size + (size/2),w.positionY*size+ (size/2)), text = w.type)
        pass
    
    def drawProduct(self, products, size):
        View.list_old.clear()
        for p in products:
            if not p.isDone:
                View.canvas.create_oval(p.positionX*size+3, p.positionY*size+3, p.positionX *size-3+size, p.positionY*size-3+size, outline="white", fill="blue", width=0)
                View.list_old.append((p.positionX, p.positionY))

        pass

    def updateProducts(self, products, size, works):
        print(products)
        print(size)
        print(works)
        for p in View.list_old:
            View.canvas.create_oval(p[0] * size + 1, p[1] * size+1, p[0] * size-1 + size, p[1] * size-1 + size, outline="gray", fill="white", width=0)
        print(View.list_old)
        self.drawWorkstations(works, size)
        self.drawProduct(products, size)
        pass

    def nextTimeStep(self, listP, listW):
        print(listW['A'])
        size = self.getSize(listW)
        self.updateProducts(listP, size, listW)

# Beispielhafte Funktionsweise
'''def main():
    list = []
    for i in range(10):
        w = Workstation('A')
        w.setPosition(i, i)
        list.append(w)

    list_p = []
    for i in range(10):
        w = Product(i, i + 1)
        list_p.append(w)



    #w = Workstation('A')
    #w.setPosition(50,30)
    #list.append(w)
    #size = ex.getSize(list)
    #ex.drawGrid(size)
    ex.drawWorkstations(list, size)
    ex.drawProduct(list_p, size)
    list_p[3].positionX  += 1
    ex.updateProducts(list_p, size, list)
    list_p[3].positionX  += 1
    ex.updateProducts(list_p, size, list)


    
    root.geometry("1000x600+300+50")
    #root.mainloop()


if __name__ == '__main__':
    main()'''