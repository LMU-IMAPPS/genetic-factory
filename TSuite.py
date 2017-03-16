from FactoryGenerator import FactoryGenerator
import numpy
import json
from Factory import visibilityStatus

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


class TSuite:
    def __init__(self, pathToFactoryRunJSON):
        with open(pathToFactoryRunJSON) as run_log:
            self.factory_run = json.load(run_log)

        with open(self.factory_run['constants']['WORKSTATION_JSON']) as workstations:
            self.workstations = json.load(workstations)

        self.factoryGenerator = FactoryGenerator(self.workstations)

        '''WSPositions Array -> back to Triplet'''
        self.factorySetting = []
        for i in range(len(self.factory_run['factorySetting'])):
            tmp = self.factory_run['factorySetting'].pop(0)
            self.factorySetting.append((tmp[0], tmp[1], tmp[2]))

    def runTest(self, products):
        fitness = []
        for p in products:
            factory = self.factoryGenerator.generateFactory(self.factorySetting,
                                                        visibilityStatus.NONE, p)
            fitness.append(factory.run())
        medianFitness = numpy.median(fitness)
        self.plotStats(medianFitness)
        print(fitness)
        print(medianFitness)


    def plotStats(self, medianFitness):
        # plot with best indiv per generation
        x = range(len(self.factory_run['plotData']))
        plt.xlabel('Time')
        plt.ylabel('Fitness')
        plt.title('Best individual over time')
        plt.plot(x, self.factory_run['plotData'], label='best', color='g')
        plt.plot((0, len(self.factory_run['plotData'])), (medianFitness, medianFitness), 'k-', label='median')
        plt.legend()
        plt.show()


testSuiteCoev = TSuite("optimizedSettings/factory_run_00.json")
randProducts = []
for i in range(10):
    randProducts.append(testSuiteCoev.factoryGenerator.generateRandomProducts(10, 5))
testSuiteCoev.runTest(randProducts)