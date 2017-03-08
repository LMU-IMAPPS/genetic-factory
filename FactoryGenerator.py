import json
from Product import Product
from Workstation import Workstation
from Factory import Factory, visibilityStatus

ARRAYSIZE = 1000

class FactoryGenerator:
    def __init__(self, path_to_products_json, path_to_workstations_json):
        # self.workStations = {}
        with open(path_to_workstations_json) as jsonFile:
            self.workstationJson = json.load(jsonFile)
        with open(path_to_products_json) as jsonFile:
            self.productsJson = json.load(jsonFile)
        self.currentFieldStatus = self.initFieldStatus()
        self.counter = 0

    def generateFactory(self, workstationPositions, visibilityType):
        ws = self.set_position_for_workstations(workstationPositions)
        p = self.generateProducts(ws)
        cfs = self.initFieldStatus()
        factory = Factory(ws, p, cfs, visibilityType)
        return factory

    def generateProducts(self, workStations):
        """ Generates products from the specified JSON file """
        products = []
        for item in self.productsJson['products']:
            products.append(Product(item['positionX'], item['positionY'], item["workstationRoute"], workStations))
        return products

    def initFieldStatus(self):
        r = []
        for i in range(0, ARRAYSIZE):
            r.append([False] * ARRAYSIZE)
        return r

    def count_workstations(self):
        """ Counts the workstations saved in FactorySimulator """
        count = 0
        for item in self.workStations.values():
            count += len(item)
        return count

    def set_position_for_workstations(self, workstation_positions):
        """ Update workstation positions with Tupel (Type, x, y) - typically from evolutionary algorithm """
        workStations = {}
        # Iterate over Workstation positions given
        for item in workstation_positions:
            if not item[0] in workStations:
                workStations.update({item[0]: []})
            # Create new Worstation object
            ws = Workstation(item[0], item[1], item[2])
            # Add time at ws constraint to ws
            for typeDef in self.workstationJson['workStations']:
                if typeDef['type'] == item[0]:
                    ws.setTimeAtWs(typeDef['time_at_ws'])
            workStations[item[0]].append(ws)
        self.checkWorkstationConstrait(workStations)
        return workStations

    def checkWorkstationConstrait(self, workStations):
        # Check number of ws types
        if not len(self.workstationJson['workStations']) == len(workStations):
            raise Exception("Workstation constrait violated")
        for item in self.workstationJson['workStations']:
            # Check count of ws for every type
            if not len(workStations[item['type']]) == item['count']:
                raise Exception("Workstation constrait violated")
