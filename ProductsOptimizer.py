import numpy
import constants

class ProductOptimizer:

    def generateRandomProductList(self):
        productList = []
        for i in range(constants.PRODUCTS_PER_LIST):
            path = ""
            for j in range(constants.PRODUCTS_PATH_LENGTH):
                workstationTypeIndex = numpy.random.randint(len(self.workstationsJson['workStations']))
                path += self.workstationsJson['workStations'][workstationTypeIndex]['type']
            productList.append((0, 0, path))
            # TODO randomize

        print(productList)
        return productList

    def __init__(self, workstationsJson):
        self.workstationsJson = workstationsJson
        self.generation = []
        for i in range(constants.LISTS_PER_GENERATION):
            self.generation.append(self.generateRandomProductList())

    def getGeneration(self):
        return self.generation

    def evaluateGeneration(self, fitnessList):
        fitnessMap = list(zip(fitnessList, self.generation))

        '''Sort'''
        #print(fitnessMap)
        fitnessMap.sort(key=lambda x: x[0], reverse=True)

        '''Select'''
        fitnessMap = fitnessMap[0:-round(len(fitnessList)/2)]

        '''Mutate'''

        '''Recombine'''

        '''Fill-up'''
        self.generation = list(zip(*fitnessMap))
        while len(self.generation) < constants.LISTS_PER_GENERATION:
            self.generation.append(self.generateRandomProductList())


