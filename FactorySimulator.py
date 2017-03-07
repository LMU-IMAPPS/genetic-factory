import json
from tkinter import Tk
from View import View
from pprint import pprint
from Product import Product
from Product import StepResult
from Workstation import Workstation
import time
import sys


class FactorySimulator:
    ARRAYSIZE = 11
    view = None

    def initFieldStatus(self):
        r = []
        for i in range(0, self.ARRAYSIZE):
            r.append([False] * self.ARRAYSIZE)
        return r

    def generate_products(self, path_to_json, workStations):
        """ Generates products from the specified JSON file """
        products = []
        with open(path_to_json) as data_file:
            data = json.load(data_file)
            for item in data['products']:
                products.append(Product(item['positionX'], item['positionY'], item["workstationRoute"], workStations))
        return products

    def generate_work_stations(self, path_to_json):
        """ Generates workstations from the specified JSON file """
        workStations = {}
        with open(path_to_json) as data_file:
            data = json.load(data_file)
            for item in data['workStations']:
                if not item['type'] in workStations:
                    # Add new Workstation type
                    workStations.update({item['type']: []})

                # Add New Workstation to List of existing type
                workStations[item['type']].append(Workstation(item['type']))
        return workStations

    def __init__(self, path_to_products_json, path_to_workstations_json):
        self.workStations = self.generate_work_stations(path_to_workstations_json)
        self.products = self.generate_products(path_to_products_json, self.workStations)
        self.currentFieldStatus = self.initFieldStatus()
        self.counter = 0
        self.viewRoot = Tk()

        """pprint(self.products)"""
        """pprint(self.workStations)"""

    def count_workstations(self):
        """ Counts the workstations saved in FactorySimulator """
        count = 0
        for item in self.workStations.values():
            count += len(item)
        return count

    def set_position_for_workstations(self, workstation_positions):
        """ Update workstation positions with Tupel (Type, x, y) - typically from evolutionary algorithm """
        # Check if length is matchig
        if self.count_workstations() == len(workstation_positions):
            # iterate over input
            for item in workstation_positions:
                # Pop, setPosition, append Workstation Objects to maintain order
                workstation = self.workStations[item[0]].pop(0)
                workstation.setPosition(item[1], item[2])
                self.workStations[item[0]].append(workstation)
        else:
            raise Exception("Too many positions in workstation_positions")

    def setup(self, workstation_positions):
        """ Sets up the factory """
        self.set_position_for_workstations(workstation_positions)
        self.View = View(self.viewRoot, self.products, self.workStations)
        self.viewRoot.geometry("1000x600+300+50")
        self.productReset()

    def productReset(self):
        for p in self.products:
            p.reset()

    def privateRun(self, vizualisationType):
        counter = 0
        while True:
            print(counter)
            madeChange = False
            isDone = True
            for p in self.products:
                result = p.run(self.currentFieldStatus)
                if not result == StepResult.BLOCKED:
                    madeChange = True
                if not result == StepResult.DONE:
                    isDone = False
            if isDone:
                if vizualisationType != 0:
                    self.View.nextTimeStep(self.products, self.workStations)
                    self.viewRoot.update()
                pprint("Done")
                return counter
            if not madeChange:
                pprint("Blocked")
                return sys.maxsize
            counter += 1
            if vizualisationType == 2:
                self.View.nextTimeStep(self.products, self.workStations)
                self.viewRoot.update()
                time.sleep(0.1)

    def run(self, viz_type):
        returnVal = []

        def innerRun():
            returnVal.append(self.privateRun(viz_type))

        self.viewRoot.after(1000, innerRun)
        self.viewRoot.mainloop()
        return returnVal[0]


Factory = FactorySimulator('Products.json', 'Workstations.json')
position_list = [('A', 3, 10), ('B', 2, 9), ('C', 7, 0), ('A', 6, 6), ('D', 1, 5)]
Factory.setup(position_list)
viz_type = 2 #0 for none, 1 for Workstation Position only, 2 for all steps
print(Factory.run(viz_type))
