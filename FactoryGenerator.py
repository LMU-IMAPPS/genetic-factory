from Product import Product
from Workstation import Workstation
from Factory import Factory
import random
import numpy


class FactoryGenerator:
    def __init__(self, workstationsJson):
        self.workstationJson = workstationsJson

    def generateRandomWorkstations(self, maxPosition):
        result = []
        for item in self.workstationJson['workStations']:
            type = item['type']
            for i in range(0, item['count']):
                result.append((type, random.randint(0, maxPosition), random.randint(0, maxPosition)))
        return result

    def generateRandomProducts(self, productsCount, pathLenght):
        productList = []
        for i in range(productsCount):
            path = ""
            for j in range(pathLenght):
                workstationTypeIndex = numpy.random.randint(len(self.workstationJson['workStations']))
                path += self.workstationJson['workStations'][workstationTypeIndex]['type']
            productList.append((0, 0, path))
        return productList

    def generateFactory(self, workstationPositions, visibilityType, products):
        ws = self.set_position_for_workstations(workstationPositions)
        p = self.generateProducts(ws, products)
        cfs = self.initFieldStatus()
        factory = Factory(ws, p, cfs, visibilityType)
        return factory

    def generateProducts(self, workStations, productList):
        """ Generates products from the specified JSON file """
        products = []
        for product in productList:
            products.append(Product(product[0], product[1], product[2], workStations))
        return products

    def initFieldStatus(self):
        return set()

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
        workStationsWaitTimes = dict()
        for ws in self.workstationJson['workStations']:
            workStationsWaitTimes[ws['type']] = ws['time_at_ws']
        for item in workstation_positions:
            if not item[0] in workStations:
                workStations.update({item[0]: []})
            # Create new Worstation object
            ws = Workstation(item[0], item[1], item[2])
            # Add time at ws constraint to ws
            ws.setTimeAtWs(workStationsWaitTimes[item[0]])
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
