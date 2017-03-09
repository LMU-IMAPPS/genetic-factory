from tkinter import Tk
from View import View
from pprint import pprint
from Product import StepResult
import time
import sys
from enum import Enum


class visibilityStatus(Enum):
    NONE = 0
    WorkstationPos = 1
    ALL = 2


class Factory:
    def __init__(self, ws, p, cfs, vs):
        self.workStations = ws
        self.products = p
        self.currentFieldStatus = cfs
        self.vs = vs
        self.View = None
        if vs != visibilityStatus.NONE:
            self.viewRoot = Tk()
            self.View = View(self.viewRoot, self.products, self.workStations, self.currentFieldStatus)
            self.viewRoot.geometry("1000x600+300+50")

    def productReset(self):
        for p in self.products:
            p.reset()

    def privateRun(self, vs):
        counter = 0
        while True:
            madeChange = False
            isDone = True
            for p in self.products:
                result = p.run(self.currentFieldStatus)
                if result == StepResult.MOVED:
                    madeChange = True
                if not result == StepResult.DONE:
                    isDone = False
            if isDone:
                if vs != visibilityStatus.NONE:
                    self.View.nextTimeStep(self.products, self.workStations)
                    self.viewRoot.update()
                    pprint("Done with Fitness "+str(counter))
                return counter
            if not madeChange:
                if vs != visibilityStatus.NONE:pprint("Blocked")
                return sys.maxsize
            counter += 1
            if vs == visibilityStatus.ALL:
                self.View.nextTimeStep(self.products, self.workStations)
                self.viewRoot.update()
                time.sleep(0.3)

    def run(self):
        returnVal = None

        def innerRun():
            nonlocal returnVal
            returnVal = self.privateRun(self.vs)

        if self.vs != visibilityStatus.NONE:
            self.viewRoot.after(1000, innerRun)
            self.viewRoot.mainloop()
        else:
            innerRun()
        return returnVal
