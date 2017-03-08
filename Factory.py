import json
from tkinter import Tk
from View import View
from pprint import pprint
from Product import Product
from Product import StepResult
from Workstation import Workstation
import time
import sys
from enum import Enum


ARRAYSIZE = 11

class visibitltyStatus(Enum):
    NONE = 0
    WorkstationPos = 1
    ALL = 2


class FactoryGenerator:

    def __init__(self, path_to_products_json, path_to_workstations_json):
        self.workStations = {}
        with open(path_to_workstations_json) as jsonFile:
            self.json = json.load(jsonFile)
        self.products = self.generate_products(path_to_products_json, self.workStations)
        self.currentFieldStatus = self.initFieldStatus()
        self.counter = 0



    def generate_products(self, path_to_json, workStations):
        """ Generates products from the specified JSON file """
        products = []
        with open(path_to_json) as data_file:
            data = json.load(data_file)
            for item in data['products']:
                products.append(Product(item['positionX'], item['positionY'], item["workstationRoute"], workStations))
        return products

   def initFieldStatus(self):
        r = []
        for i in range(0, self.ARRAYSIZE):
            r.append([False] * self.ARRAYSIZE)
        return r


    def count_workstations(self):
        """ Counts the workstations saved in FactorySimulator """
        count = 0
        for item in self.workStations.values():
            count += len(item)
        return count


    def set_position_for_workstations(self, workstation_positions):
        """ Update workstation positions with Tupel (Type, x, y) - typically from evolutionary algorithm """
        # Clear Workstation info from previous run
        self.workStations.clear()
        # Iterate over Workstation positions given
        for item in workstation_positions:
            if not item[0] in self.workStations:
                self.workStations.update({item[0]: []})
            # Create new Worstation object
            ws = Workstation(item[0], item[1], item[2])
            # Add time at ws constraint to ws
            for typeDef in self.json['workStations']:
                if typeDef['type'] == item[0]:
                    ws.setTimeAtWs(typeDef['time_at_ws'])

            self.workStations[item[0]].append(ws)


    def setup(self, workstation_positions):
        """ Sets up the factory """
        self.set_position_for_workstations(workstation_positions)
        self.productReset()


    def checkWorksta_to_ptionConstrait(self):
        # Check number of ws types
        if not len(self.json['workStations']) == len(self.workStations):
            raise Exception("Workstation constrait violated")
        for item in self.json['workStations']:
            # Check count of ws for every type
            if not len(self.workStations[item['type']]) == item['count']:
                raise Exception("Workstation constrait violated")


class Factory:

    def __init__(self, ws, p, cfs, c, vs):
        self.workStations = ws
        self.products = p
        self.currentFieldStatus = cfs
        self.counter = c
        self.vs = vs
        self.View = None
        if vs != visibitltyStatus.NONE:
            self.viewRoot = Tk()
            self.View = View(self.viewRoot, self.products, self.workStations)
            self.viewRoot.geometry("1000x600+300+50")




    def productReset(self):
        for p in self.products:
            p.reset()

    def privateRun(self, vs):
        counter = 0
        while True:
            print(counter)
            madeChange = False
            isDone = True
            for p in self.products:
                result = p.run(self.currentFieldStatus)
                if result == StepResult.MOVED:
                    madeChange = True
                if not result == StepResult.DONE:
                    isDone = False
            if isDone:
                if vs != visibitltyStatus.NONE:
                    self.View.nextTimeStep(self.products, self.workStations)
                    self.viewRoot.update()
                pprint("Done")
                return counter
            if not madeChange:
                pprint("Blocked")
                return sys.maxsize
            counter += 1
            if vs == visibitltyStatus.ALL:
                self.View.nextTimeStep(self.products, self.workStations)
                self.viewRoot.update()
                time.sleep(0.1)

    def run(self):
        returnVal = None

        def innerRun():
            nonlocal returnVal
            returnVal = self.privateRun(self.vs)

        if self.vs != visibitltyStatus.NONE:
            self.viewRoot.after(1000, innerRun)
            self.viewRoot.mainloop()
        else:
            innerRun()
        return returnVal

viz_type = visibitltyStatus.NONE
facGen = FactoryGenerator('Products.json', 'Workstations.json', viz_type)
position_list = [('A', 3, 10), ('B', 2, 9), ('C', 7, 0), ('A', 6, 6), ('D', 1, 5)]

Factory.setup(position_list)
print(Factory.run())
