from tkinter import Tk, Canvas, Frame, BOTH
from Workstation import Workstation
from random import randint

class View(Frame):
    
    canvas = None
 
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()     
        
    def initUI(self):
      
        self.parent.title("IMAPS")        
        self.pack(fill=BOTH, expand=1)
    
        View.canvas = Canvas(self,bg ="white")
        View.canvas.pack(fill=BOTH, expand=1)
        
    def drawGrid(self, inputarray):
        tX = 5
        tY = 5
        size = 10
        if(600/len(inputarray) > 1000/len(inputarray[0])):
            size = 1000/len(inputarray[0])
        else:
            size = 600/len(inputarray[0])
        for i in range(len(inputarray)):
            for j in range(len(inputarray[i])):
                color = "blue"
                
                if (inputarray[i][j] == False):
                    color = "red"
                    View.canvas.create_text((i*size +tX + (size/2),j*size+tY + (size/2)), text = "A")
                View.canvas.create_rectangle(i*size +tX,j*size+tY,(i*size)+size+tY,(j*size)+size+tY, fill=color)
                
    def getSize(self, works):
        size = 0
        minX = 10000
        maxX = 0
        minY = 10000
        maxY = 0
        for w in works:
            if(w.positionX < minX):
                minX = w.positionX
            if(w.positionX > maxX):
                maxX = w.positionX
            if(w.positionY < minY):
                minY = w.positionY
            if(w.positionY > maxY):
                maxY = w.positionY
                
        if(1000.0/(1+(maxX-minX)) > 600.0/(1+(maxY-minY))):
            size = 600.0/(1+(maxY-minY))
        else:
            size = 1000.0/(1+(maxX-minX))
        
        return size   
                
    def drawWorkstations(self, works, size):
        for w in works:
            View.canvas.create_rectangle(w.positionX*size , w.positionY*size, w.positionX*size+size,w.positionY*size+size, fill="pink")
            View.canvas.create_text((w.positionX*size + (size/2),w.positionY*size+ (size/2)), text = w.type)
        pass
    
    def drawProduct(self, products, size):
        pass
    
    def updateProducts(self, products):
        pass

def main():
  
    root = Tk()
    ex = View(root)
    list = []
    for i in range(10):
        w = Workstation('A')
        w.setPosition(i,i)
        list.append(w)
    
    #w = Workstation('A')
    #w.setPosition(50,30)
    #list.append(w)
    size = ex.getSize(list)
    ex.drawWorkstations(list, size)
    #ex.drawGrid(list)
    
    root.geometry("1000x600+300+50")
    root.mainloop()  


if __name__ == '__main__':
    main() 