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
            factory = self.factoryGenerator.generateFactory(self.factorySetting, visibilityStatus.NONE, p)
            fitness.append(factory.run())
        medianFitness = numpy.median(fitness)
        lowerBound = numpy.percentile(fitness, 25)
        upperBound = numpy.percentile(fitness, 75)
        self.plotStats(medianFitness, lowerBound, upperBound)
        print(fitness)
        print(medianFitness)

    def plotStats(self, medianFitness, lowerBound, upperBound):
        # plot best individual per generation
        blockedFitness = 1_844_674_407_370_955_264
        worst = 0
        for i in range(len(self.factory_run['plotData'])):
            if (self.factory_run['plotData'][i] < blockedFitness) and (self.factory_run['plotData'][i] > worst):
                worst = self.factory_run['plotData'][i]
        blocked = worst + 5
        for i in range(len(self.factory_run['plotData'])):
            if self.factory_run['plotData'][i] >= blockedFitness:
                self.factory_run['plotData'][i] = blocked
        threshold = [worst + 5.2] * len(self.factory_run['plotData'])
        x = range(len(self.factory_run['plotData']))
        plt.xlabel('Time')
        plt.ylabel('Fitness')
        plt.title('Best individual over time')
        plt.plot(x, self.factory_run['plotData'], label='best', color='g')

        # draw line for blocked value
        plt.plot(x, threshold, label='blocked', color='r')

        # draw line for test result (median)
        if medianFitness >= blocked:
            medianFitness = blocked
        plt.plot((0, len(self.factory_run['plotData'])), (medianFitness, medianFitness), 'k-', label='median')

        # draw line for upper and lower bound of test result
        if lowerBound >= blocked:
            lowerBound = blocked
        plt.plot((0, len(self.factory_run['plotData'])), (lowerBound, lowerBound), 'k-')
        if upperBound >= blocked:
            upperBound = blocked
        plt.plot((0, len(self.factory_run['plotData'])), (upperBound, upperBound), 'k-')
        plt.legend()
        plt.show()

        # plot diversity of best individual per generation
        ypos = range(len(self.factory_run['plotDiversity']))
        mean = numpy.mean(self.factory_run['plotDiversity'])
        plt.plot(ypos, self.factory_run['plotDiversity'], color='g')
        plt.plot((0, len(self.factory_run['plotDiversity'])), (mean, mean), 'k-', label='mean')
        plt.ylabel('Diversity')
        plt.xlabel('Time')
        plt.title('Diversity of best individual over time')
        plt.show()


''' TEST: coevolution vs. no coevolution '''
testSuiteCoev = TSuite("optimizedSettings/factory_run_01.json")
testSuiteNoCoev = TSuite("optimizedSettings/factory_run_02.json")
randProducts = []
product_path_length = testSuiteCoev.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuiteCoev.factory_run['constants']['PRODUCTS_PER_LIST']
for i in range(20):
    randProducts.append(testSuiteCoev.factoryGenerator.generateRandomProducts(products_per_list, product_path_length))
testSuiteCoev.runTest(randProducts)
testSuiteNoCoev.runTest(randProducts)

''' TEST: different mutation rates 0.1 0.5 0.9 '''
testSuiteMut01 = TSuite("optimizedSettings/factory_run_03.json")
testSuiteMut05 = TSuite("optimizedSettings/factory_run_04.json")
testSuiteMut09 = TSuite("optimizedSettings/factory_run_05.json")
randProducts = []
product_path_length = testSuiteMut01.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuiteMut01.factory_run['constants']['PRODUCTS_PER_LIST']
for i in range(100):
    randProducts.append(testSuiteMut01.factoryGenerator.generateRandomProducts(products_per_list, product_path_length))
testSuiteMut01.runTest(randProducts)
testSuiteMut05.runTest(randProducts)
testSuiteMut09.runTest(randProducts)


