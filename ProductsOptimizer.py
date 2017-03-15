import numpy
import constants
from EvilProducts import EvilProducts
import math

class ProductOptimizer:

    def evilProductsSelection(self):
        '''Sort'''
        self.generation.sort(key=lambda y: y.fitness, reverse=True)

        ''' Return sublist with best <SELECTION_FACTOR> from generation '''
        nextGeneration = []
        lenGeneration = len(self.generation)
        for i in range(lenGeneration):
            if pow(i / lenGeneration, 1 / (constants.PRODUCTS_SELECTION_FACTOR * 2)) <= numpy.random.random():
                nextGeneration.append(self.generation[i])
        return nextGeneration

    ''' Generate inital random EvilProducs individual '''
    def generateEvilProducts(self):
        productList = []
        for i in range(constants.PRODUCTS_PER_LIST):
            path = ""
            for j in range(constants.PRODUCTS_PATH_LENGTH):
                workstationTypeIndex = numpy.random.randint(len(self.workstationsJson['workStations']))
                path += self.workstationsTypes[workstationTypeIndex]
            productList.append((0, 0, path))
            # TODO randomize

    def generateEvilProduct(self, productList):
        return EvilProducts(productList, self.generateAdditionalWaitTimesList())

    def __init__(self, workstationsJson, factoryGenerator):
        self.workstationsJson = workstationsJson
        self.workstationsTypes = []
        for ws in workstationsJson['workStations']:
            self.workstationsTypes.append(ws['type'])
        self.factoryGenerator = factoryGenerator
        ''' Initialize random EvilProducts population '''
        self.generation = []
        for i in range(constants.LISTS_PER_GENERATION):
            positionList = self.factoryGenerator.generateRandomProducts(constants.PRODUCTS_PER_LIST, constants.PRODUCTS_PATH_LENGTH)
            self.generation.append(self.generateEvilProduct(positionList))

    def generateAdditionalWaitTimesList(self):
        result = []
        for i in range(constants.ADDITIONAL_WAIT_TIMES_COUNT):
            result.append(self.workstationsTypes[numpy.random.randint(0, len(self.workstationsTypes))])
        return result


    def getGeneration(self):
        return self.generation

#-----------------------------------------------------------------------------------------
    def evaluateGeneration(self):
        '''Select'''
        self.generation = self.evilProductsSelection()

        '''Mutate'''
        for evilProduct in self.generation:
            evilProduct.mutate(constants.PRODUCTS_MUTATION_FACTOR, self.workstationsJson, self.workstationsTypes)

        '''Recombine'''

        for i in range(int(constants.PRODUCTS_RECOMBINATION_FACTOR*len(self.generation))):
            ancestorIndex1 = 0
            ancestorIndex2 = 0
            while ancestorIndex1 == ancestorIndex2:
                ancestorIndex1 = numpy.random.randint(0, len(self.generation))
                ancestorIndex2 = numpy.random.randint(0, len(self.generation))
            self.generation.append(EvilProducts.recombine(self.generation[ancestorIndex1], self.generation[ancestorIndex2]))

        '''Fill-up'''
        while len(self.generation) < constants.LISTS_PER_GENERATION:
            positionList = self.factoryGenerator.generateRandomProducts(constants.PRODUCTS_PER_LIST, constants.PRODUCTS_PATH_LENGTH)
            self.generation.append(self.generateEvilProduct(positionList))



