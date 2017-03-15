import numpy
import constants
from EvilProducts import EvilProducts

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
    def generateEvilProduct(self, productList):
        return EvilProducts(productList)

    def __init__(self, workstationsJson, factoryGenerator):
        self.workstationsJson = workstationsJson
        self.factoryGenerator = factoryGenerator
        ''' Initialize random EvilProducts population '''
        self.generation = []
        for i in range(constants.LISTS_PER_GENERATION):
            positionList = self.factoryGenerator.generateRandomProducts(constants.PRODUCTS_PER_LIST, constants.PRODUCTS_PATH_LENGTH)
            self.generation.append(self.generateEvilProduct(positionList))

    def getGeneration(self):
        return self.generation

    def evaluateGeneration(self):
        '''Select'''
        self.generation = self.evilProductsSelection()

        '''Mutate'''
        for evilProduct in self.generation:
            evilProduct.mutate(constants.PRODUCTS_MUTATION_FACTOR, self.workstationsJson)

        '''Recombine'''
        #for i in range(int(constants.RECOMBINATION_FACTOR*len(self.generation))):
        #    ancestorIndex1 = 0
        #    ancestorIndex2 = 0
        #    while ancestorIndex1 == ancestorIndex2:
        #        ancestorIndex1 = numpy.random.randint(0, len(self.generation))
        #        ancestorIndex2 = numpy.random.randint(0, len(self.generation))
        #    self.generation.append(EvilProducts.recombine(self.generation[ancestorIndex1], self.generation[ancestorIndex2]))

        '''Fill-up'''
        while len(self.generation) < constants.LISTS_PER_GENERATION:
            positionList = self.factoryGenerator.generateRandomProducts(constants.PRODUCTS_PER_LIST, constants.PRODUCTS_PATH_LENGTH)
            self.generation.append(self.generateEvilProduct(positionList))



