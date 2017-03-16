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
            if (self.factory_run['plotData'][i] != blockedFitness) and (self.factory_run['plotData'][i] > worst):
                worst = self.factory_run['plotData'][i]
        blocked = worst + 5
        for i in range(len(self.factory_run['plotData'])):
            if self.factory_run['plotData'][i] == blockedFitness:
                self.factory_run['plotData'][i] = blocked
        threshold = [worst + 5.2] * len(self.factory_run['plotData'])
        x = range(len(self.factory_run['plotData']))

        matplotlib.rc('axes', facecolor='#263238', edgecolor='#B0BEC5', labelcolor='#CFD8DC')
        matplotlib.rc('figure', facecolor='#37474F', edgecolor='#B0BEC5')
        matplotlib.rc('savefig', facecolor='#37474F', edgecolor='#B0BEC5')
        matplotlib.rc('patch', edgecolor='#B0BEC5')
        matplotlib.rc('xtick', color='#B0BEC5')
        matplotlib.rc('ytick', color='#B0BEC5')
        matplotlib.rc('lines', color='#B0BEC5')
        matplotlib.rc('text', color='#B0BEC5')
        matplotlib.rc('grid', color='#B0BEC5')

        # Draw Horizontal line
        #plt.axhline(linewidth=4, color='r')

        plt.xlabel('Cycle')
        plt.ylabel('Fitness')
        plt.title('Best individual over time')
        plt.plot(x, self.factory_run['plotData'], label='best', color='#3F51B5')

        # draw line for blocked value
        plt.plot(x, threshold, label='blocked', color='#F44336')

        # draw line for test result (median)
        if medianFitness >= blockedFitness:
            medianFitness = blocked
        plt.plot((0, len(self.factory_run['plotData'])), (medianFitness, medianFitness), 'k-', label='median', color='#ECEFF1')

        # draw line for upper and lower bound of test result
        if lowerBound >= blockedFitness:
            lowerBound = blocked
        plt.plot((0, len(self.factory_run['plotData'])), (lowerBound, lowerBound), 'k-', color='#607D8B')
        if upperBound >= blockedFitness:
            upperBound = blocked
        plt.plot((0, len(self.factory_run['plotData'])), (upperBound, upperBound), 'k-', color='#607D8B')

        plt.legend()
        plt.show()

        # plot diversity of best individual per generation
        '''ypos = range(len(self.factory_run['plotDiversity']))
        plt.plot(ypos, self.factory_run['plotDiversity'], color='g')
        plt.ylabel('Diversity')
        plt.xlabel('Time')
        plt.title('Diversity of best individual over time')
        plt.show()'''

        '''figure = Figure()
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot(1, 1, 1, axisbg='red')
        axes.plot([1, 2, 3])'''''


''' TEST: Coevolution vs. No Coevolution '''
testSuiteCoev = TSuite("optimizedSettings/factory_run_01.json")
testSuiteNoCoev = TSuite("optimizedSettings/factory_run_02.json")
randProducts = []
product_path_length = testSuiteCoev.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuiteCoev.factory_run['constants']['PRODUCTS_PER_LIST']

for i in range(20):
    randProducts.append(testSuiteCoev.factoryGenerator.generateRandomProducts(products_per_list, product_path_length))
testSuiteCoev.runTest(randProducts)
testSuiteNoCoev.runTest(randProducts)

''' TEST: XXX '''