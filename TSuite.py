from FactoryGenerator import FactoryGenerator
import numpy
import json
import sys
from enum import Enum
from Factory import visibilityStatus

import matplotlib

from matplotlib import pyplot as plt


class PlotType(Enum):
    PLOT = plt.plot
    SCATTER = plt.scatter
    BAR = plt.bar


class Plot(Enum):
    NONE = 0
    FITNESS = 1
    DIVERSITY = 2
    ALL = 3


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

    def runTest(self, products, plot):
        fitness = []
        for p in products:
            factory = self.factoryGenerator.generateFactory(self.factorySetting, visibilityStatus.NONE, p)
            fitness.append(factory.run())
        medianFitness = numpy.median(fitness)
        lowerBound = numpy.percentile(fitness, 25)
        upperBound = numpy.percentile(fitness, 75)

        '''Draw plots '''
        if plot == Plot.ALL:
            self.plotStats(self.factory_run['plotData'], medianFitness, lowerBound, upperBound, "Cycles", "Fitness",
                           "Best individual over time", PlotType.PLOT, self.factory_run['constants'])
            self.plotDiversity(self.factory_run['constants'])
        if plot == Plot.DIVERSITY:
            self.plotStats(self.factory_run['plotData'], medianFitness, lowerBound, upperBound, "Cycles", "Fitness",
                           "Best individual over time", PlotType.PLOT, self.factory_run['constants'])
        if plot == Plot.DIVERSITY:
            self.plotDiversity(self.factory_run['constants'])

        # '''Output result in console'''
        # print("     Fitness: ", fitness)
        # print("     Median:  ", medianFitness)
        # print("    ----------------------------------------------------------------------------------------------------------------------------------------------------------")

        return fitness, medianFitness

    def plotStats(self, fitness, medianFitness, lowerBound, upperBound, xlable, ylable, title, plotType, constants):
        # plot best individual per generation
        blockedFitness = 1_844_674_407_370_955_264
        worst = 0
        for i in range(len(fitness)):
            if (fitness[i] < blockedFitness) and (fitness[i] > worst):
                worst = fitness[i]
        blocked = worst + 5
        for i in range(len(fitness)):
            if fitness[i] >= blockedFitness:
                fitness[i] = blocked
        x = range(1, len(fitness) + 1)

        matplotlib.rc('axes', facecolor='#263238', edgecolor='#B0BEC5', labelcolor='#CFD8DC')
        matplotlib.rc('figure', facecolor='#37474F', edgecolor='#B0BEC5')
        matplotlib.rc('savefig', facecolor='#37474F', edgecolor='#B0BEC5')
        matplotlib.rc('patch', edgecolor='#B0BEC5')
        matplotlib.rc('xtick', color='#B0BEC5')
        matplotlib.rc('ytick', color='#B0BEC5')
        matplotlib.rc('lines', color='#B0BEC5')
        matplotlib.rc('text', color='#B0BEC5')
        matplotlib.rc('grid', color='#B0BEC5')

        plt.xlabel(xlable)
        plt.ylabel(ylable)
        text = title + "\n"
        plt.title(text)

        plotType(x, fitness, label='best', color='#3F51B5')

        # draw line for blocked value
        plt.plot((0, len(fitness)), (blocked + 0.2, blocked + 0.2), label='blocked', color='#F44336')

        # draw line for test result (median)
        if medianFitness >= blocked:
            medianFitness = blocked
        plt.plot((0, len(fitness)), (medianFitness, medianFitness), 'k-', label='median', color='#ECEFF1')

        # draw line for upper and lower bound of test result
        if lowerBound >= blocked:
            lowerBound = blocked
        plt.plot((0, len(fitness)), (lowerBound, lowerBound), 'k-', color='#607D8B')
        if upperBound >= blocked:
            upperBound = blocked
        plt.plot((0, len(fitness)), (upperBound, upperBound), 'k-', color='#607D8B')

        # draw line for test result (median)
        if medianFitness >= blocked:
            medianFitness = blocked
        plt.plot((0, len(fitness)), (medianFitness, medianFitness), 'k-', label='median', color='#ECEFF1')

        # write constants into graph
        text = "Cycles = " + str(constants['EVOLUTION_CYCLES']) + "\nCoevolution = " + str(constants['COEVOLUTION_ON']) + "\nPopulation = " + str(constants['POPULATION_SIZE']) + "\nSelection = " + str(constants['SELECTION_FACTOR']) + "\nMutation = " + str(constants['MUTATION_FACTOR']) + "\nRecombination = " + str(constants['RECOMBINATION_FACTOR'])
        plt.annotate(text, xy=(1.05, 0.5), xycoords='axes fraction', bbox=dict(boxstyle="round", fc='#263238'))

        plt.legend(loc="center left", bbox_to_anchor=(0, -0.12), ncol=3)

        plt.subplots_adjust(left=0.1, bottom=0.15, right=0.79, top=0.9, wspace=0.2, hspace=0.2)
        plt.show()

    def plotDiversity(self, constants):
        # plot diversity of best individual per generation
        ypos = range(len(self.factory_run['plotDiversity']))
        mean = numpy.mean(self.factory_run['plotDiversity'])
        plt.plot(ypos, self.factory_run['plotDiversity'], label='diversity', color='g')
        plt.plot((0, len(self.factory_run['plotDiversity'])), (mean, mean), 'k-', label='mean', color='#ECEFF1')
        plt.ylabel('Diversity')
        plt.xlabel('Time')
        plt.title('Diversity of best individual over time')

        # write constants into graph
        text = "Cycles = " + str(constants['EVOLUTION_CYCLES']) + "\nCoevolution = " + str(
            constants['COEVOLUTION_ON']) + "\nPopulation = " + str(
            constants['POPULATION_SIZE']) + "\nSelection = " + str(
            constants['SELECTION_FACTOR']) + "\nMutation = " + str(
            constants['MUTATION_FACTOR']) + "\nRecombination = " + str(constants['RECOMBINATION_FACTOR'])
        plt.annotate(text, xy=(1.05, 0.5), xycoords='axes fraction', bbox=dict(boxstyle="round", fc='#263238'))

        plt.legend(loc="center left", bbox_to_anchor=(0, -0.12), ncol=3)

        plt.subplots_adjust(left=0.1, bottom=0.15, right=0.79, top=0.9, wspace=0.2, hspace=0.2)
        plt.show()


# TEST: coevolution vs. no coevolution

print(
    "##############################################################################################################################################################\n"
    "TEST: coevolution vs. no coevolution\n"
    "##############################################################################################################################################################\n")
testSuiteCoev = TSuite("optimizedSettings/.factory_run_01.json")
testSuiteNoCoev = TSuite("optimizedSettings/.factory_run_02.json")
randProducts = []
product_path_length = testSuiteCoev.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuiteCoev.factory_run['constants']['PRODUCTS_PER_LIST']
for i in range(10):
    randProducts.append(testSuiteCoev.factoryGenerator.generateRandomProducts(products_per_list, product_path_length))
# testSuiteCoev.runTest(randProducts, Plot.NONE)
# testSuiteNoCoev.runTest(randProducts, Plot.NONE)


# TEST: different mutation rates 0.1 0.5 0.9

print(
    "##############################################################################################################################################################\n"
    "TEST: different mutation rates 0.1 0.5 0.9\n"
    "##############################################################################################################################################################\n")
testSuiteMut01 = TSuite("optimizedSettings/.factory_run_03.json")
testSuiteMut05 = TSuite("optimizedSettings/.factory_run_04.json")
testSuiteMut09 = TSuite("optimizedSettings/.factory_run_05.json")
randProducts = []
product_path_length = testSuiteMut01.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuiteMut01.factory_run['constants']['PRODUCTS_PER_LIST']
for i in range(10):
    randProducts.append(testSuiteMut01.factoryGenerator.generateRandomProducts(products_per_list, product_path_length))
# testSuiteMut01.runTest(randProducts, Plot.NONE)
# testSuiteMut05.runTest(randProducts, Plot.NONE)
# testSuiteMut09.runTest(randProducts, Plot.NONE)


# TEST: different evolution cycles for optimization with no coevolution

print(
    "##############################################################################################################################################################\n"
    "TEST: different evolution cycles for optimization with no coevolution 10 100 250\n"
    "##############################################################################################################################################################\n")
testSuite10 = TSuite("optimizedSettings/.factory_run_06.json")
testSuite100 = TSuite("optimizedSettings/.factory_run_07.json")
testSuite250 = TSuite("optimizedSettings/.factory_run_08.json")

randProducts = []
product_path_length = testSuite10.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuite10.factory_run['constants']['PRODUCTS_PER_LIST']
for i in range(10):
    randProducts.append(testSuite10.factoryGenerator.generateRandomProducts(products_per_list, product_path_length))
#testSuite10.runTest(randProducts, Plot.ALL)
#testSuite100.runTest(randProducts, Plot.ALL)
#testSuite250.runTest(randProducts, Plot.ALL)


''''# TEST: median test result for multiple optimization with and without coevolution

print(
    "##############################################################################################################################################################\n"
    "TEST: median test result for multiple optimization with and without coevolution\n"
    "##############################################################################################################################################################\n")
medianResultsNoCoev = []
medianResultsCoev = []
randProducts = []
testSuiteM = TSuite("optimizedSettings/factoryRuns/withoutCoevolution/factory_run_00.json")
product_path_length = testSuiteM.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuiteM.factory_run['constants']['PRODUCTS_PER_LIST']
for j in range(1000):
    randProducts.append(testSuiteM.factoryGenerator.generateRandomProducts(products_per_list, product_path_length))
# Test optimization without coevolution
for i in range(200):
    if i < 10:
        name = "optimizedSettings/factoryRuns/withoutCoevolution/factory_run_0" + str(i) + ".json"
    else:
        name = "optimizedSettings/factoryRuns/withoutCoevolution/factory_run_" + str(i) + ".json"
    testSuiteM = TSuite(name)
    medianResultsNoCoev.append(testSuiteM.runTest(randProducts, Plot.NONE)[1])

    #See whats going on in the console
    percentage = round(i / 200 * 100)
    bar = "[" + "=" * round(percentage / 2) + "-" * round(50 - (percentage / 2)) + "]"
    sys.stdout.write("Progress: \r%d%% Done \t %s \tMedian test result for current workstation %i" % (percentage, bar, medianResultsNoCoev[i]))
    sys.stdout.flush()

medianNoCoev = numpy.median(medianResultsNoCoev)
lowerBoundNoCoev = numpy.percentile(medianResultsNoCoev, 25)
upperBoundNoCoev = numpy.percentile(medianResultsNoCoev, 75)

    # Test optimizations with coevolution
for i in range(200):
    if i < 10:
        name = "optimizedSettings/factoryRuns/withCoevolution/factory_run_0" + str(i) + ".json"
    else:
        name = "optimizedSettings/factoryRuns/withCoevolution/factory_run_" + str(i) + ".json"
    testSuiteN = TSuite(name)
    medianResultsCoev.append(testSuiteN.runTest(randProducts, Plot.NONE)[1])

    #See whats going on in the console
    percentage = round(i / 200 * 100)
    bar = "[" + "=" * round(percentage / 2) + "-" * round(50 - (percentage / 2)) + "]"
    sys.stdout.write("Progress: \r%d%% Done \t %s \tMedian test result for current workstation %i" % (percentage, bar, medianResultsCoev[i]))
    sys.stdout.flush()

medianCoev = numpy.median(medianResultsCoev)
lowerBoundCoev = numpy.percentile(medianResultsCoev, 25)
upperBoundCoev = numpy.percentile(medianResultsCoev, 75)

print("Coevolution OFF:")
print("  Result: ", medianResultsNoCoev)
print("  Median: ", medianNoCoev)
print("Coevolution ON:")
print("  Result: ", medianResultsCoev)
print("  Median: ", medianCoev)

testSuiteM.plotStats(medianResultsNoCoev, medianNoCoev, lowerBoundNoCoev, upperBoundNoCoev, "Run", "Result",
                     "Results of multiple test runs without coevolution", PlotType.BAR, testSuiteM.factory_run['constants'])
testSuiteN.plotStats(medianResultsCoev, medianCoev, lowerBoundCoev, upperBoundCoev, "Run", "Result",
                     "Results of multiple test runs with coevolution", PlotType.BAR, testSuiteN.factory_run['constants'])
testSuiteM.plotStats(medianResultsNoCoev, medianNoCoev, lowerBoundNoCoev, upperBoundNoCoev, "Run", "Result",
                     "Results of multiple test runs without coevolution", PlotType.SCATTER, testSuiteM.factory_run['constants'])
testSuiteN.plotStats(medianResultsCoev, medianCoev, lowerBoundCoev, upperBoundCoev, "Run", "Result",
                     "Results of multiple test runs with coevolution", PlotType.SCATTER, testSuiteN.factory_run['constants'])
'''

# TEST: median test result for multiple optimization with and without coevolution

print(
    "##############################################################################################################################################################\n"
    "TEST: median test result for multiple optimization with and without coevolution\n"
    "##############################################################################################################################################################\n")
testSuiteM = TSuite("optimizedSettings/factoryRuns/withoutCoevolution/factory_run_00.json")
testSuiteN = TSuite("optimizedSettings/factoryRuns/withCoevolution/factory_run_00.json")
product_path_length = testSuiteM.factory_run['constants']['PRODUCTS_PATH_LENGTH']
products_per_list = testSuiteM.factory_run['constants']['PRODUCTS_PER_LIST']

medianResultsNoCoev =  [105.0, 99.0, 106.0, 108.0, 103.0, 96.0, 105.0, 100.0, 100.0, 106.0, 111.0, 113.0, 9.2233720368547758e+18, 121.0, 99.0, 103.0, 103.0, 111.0, 105.0, 111.0, 103.0, 134.0, 115.0, 102.0, 112.0, 103.0, 101.0, 99.0, 113.0, 108.0, 108.0, 111.0, 108.0, 103.0, 107.0, 98.0, 116.0, 110.0, 96.0, 113.0, 102.0, 111.0, 102.0, 106.0, 103.0, 109.0, 100.0, 102.5, 105.0, 121.0, 103.0, 119.0, 105.0, 102.0, 98.0, 111.0, 105.0, 104.0, 103.0, 9.2233720368547758e+18, 114.0, 100.0, 99.0, 102.0, 105.0, 102.0, 109.0, 113.0, 116.0, 117.0, 101.0, 101.0, 108.0, 111.0, 103.0, 99.0, 108.0, 118.0, 99.0, 103.0, 111.0, 135.0, 117.0, 102.0, 9.2233720368547758e+18, 110.0, 105.0, 9.2233720368547758e+18, 102.0, 105.0, 106.0, 109.0, 105.0, 114.0, 100.0, 109.0, 106.0, 111.0, 123.0, 105.0, 106.0, 108.0, 109.0, 106.0, 119.0, 131.5, 99.0, 127.0, 101.0, 136.0, 104.0, 101.0, 9.2233720368547758e+18, 117.0, 105.0, 98.0, 9.2233720368547758e+18, 103.0, 101.0, 100.0, 103.0, 101.0, 98.0, 116.0, 99.0, 108.0, 111.0, 110.0, 108.0, 102.0, 111.0, 104.0, 106.0, 101.0, 138.0, 108.0, 110.0, 98.0, 121.0, 101.0, 110.0, 110.0, 107.0, 115.0, 102.0, 103.0, 106.0, 114.0, 109.0, 119.5, 111.0, 100.0, 9.2233720368547758e+18, 106.0, 106.0, 98.0, 111.5, 99.0, 102.0, 111.0, 106.0, 102.0, 102.0, 106.0, 111.0, 114.0, 114.5, 104.5, 119.0, 100.0, 114.5, 113.0, 100.0, 99.0, 109.0, 109.0, 9.2233720368547758e+18, 103.0, 117.0, 101.0, 109.0, 101.0, 97.5, 99.0, 111.0, 118.0, 102.0, 98.0, 9.2233720368547758e+18, 104.0, 9.2233720368547758e+18, 9.2233720368547758e+18, 106.0, 111.0, 108.0, 98.0, 101.0, 104.0, 9.2233720368547758e+18, 108.5]
medianNoCoev = 106.0
lowerBoundNoCoev = numpy.percentile(medianResultsNoCoev, 25)
upperBoundNoCoev = numpy.percentile(medianResultsNoCoev, 75)

medianResultsCoev = [101.0, 101.0, 110.0, 105.5, 105.0, 106.0, 98.0, 100.0, 105.0, 109.0, 106.0, 100.0, 104.0, 102.0, 101.0, 113.0, 103.0, 101.0, 104.0, 102.0, 108.0, 100.0, 103.0, 107.0, 99.0, 101.0, 109.0, 102.0, 109.0, 99.0, 102.0, 103.0, 99.0, 111.0, 107.0, 115.0, 105.0, 104.0, 100.0, 100.0, 106.0, 110.0, 99.0, 106.0, 104.0, 105.0, 104.0, 102.0, 108.0, 103.0, 103.0, 106.0, 104.0, 102.0, 101.5, 105.0, 104.0, 101.0, 113.0, 99.0, 98.0, 102.0, 99.0, 103.0, 108.0, 99.0, 105.0, 109.0, 106.0, 104.0, 110.0, 107.0, 101.0, 102.0, 104.0, 106.5, 109.0, 107.0, 109.0, 101.0, 111.0, 102.0, 110.0, 99.0, 102.0, 109.0, 105.0, 103.0, 103.0, 102.0, 103.0, 102.0, 108.0, 107.5, 104.0, 105.0, 99.0, 110.0, 105.0, 107.0, 108.0, 106.0, 108.0, 101.0, 110.0, 112.0, 105.0, 103.0, 104.0, 104.5, 107.0, 114.0, 100.0, 104.0, 114.0, 106.0, 100.0, 105.0, 98.0, 111.0, 103.0, 105.0, 105.0, 99.0, 105.5, 107.0, 107.0, 100.0, 102.0, 102.0, 104.0, 105.0, 111.0, 106.0, 105.0, 99.0, 112.0, 114.0, 109.0, 104.0, 103.0, 102.0, 103.0, 104.5, 108.0, 112.0, 103.5, 101.0, 101.0, 100.0, 100.0, 105.0, 103.0, 105.0, 102.0, 102.0, 103.0, 102.0, 103.0, 100.0, 107.0, 104.0, 101.0, 107.0, 104.0, 140.0, 106.0, 103.0, 103.0, 99.0, 102.0, 104.0, 109.0, 102.0, 102.0, 100.0, 105.0, 100.0, 103.0, 102.0, 106.0, 103.0, 101.0, 107.0, 106.0, 101.0, 104.0, 106.0, 110.0, 108.0, 101.0, 103.0, 104.0, 109.0, 105.0, 106.0, 103.0, 103.0, 102.0, 99.0]
medianCoev = 102.0
lowerBoundCoev = numpy.percentile(medianResultsCoev, 25)
print(lowerBoundCoev)
upperBoundCoev = numpy.percentile(medianResultsCoev, 75)
print(upperBoundCoev)

testSuiteM.plotStats(medianResultsNoCoev, medianNoCoev, lowerBoundNoCoev, upperBoundNoCoev, "Run", "Result",
                     "Results of multiple test runs without coevolution", PlotType.BAR, testSuiteM.factory_run['constants'])
testSuiteN.plotStats(medianResultsCoev, medianCoev, lowerBoundCoev, upperBoundCoev, "Run", "Result",
                     "Results of multiple test runs with coevolution", PlotType.BAR, testSuiteN.factory_run['constants'])
testSuiteM.plotStats(medianResultsNoCoev, medianNoCoev, lowerBoundNoCoev, upperBoundNoCoev, "Run", "Result",
                     "Results of multiple test runs without coevolution", PlotType.SCATTER, testSuiteM.factory_run['constants'])
testSuiteN.plotStats(medianResultsCoev, medianCoev, lowerBoundCoev, upperBoundCoev, "Run", "Result",
                     "Results of multiple test runs with coevolution", PlotType.SCATTER, testSuiteN.factory_run['constants'])