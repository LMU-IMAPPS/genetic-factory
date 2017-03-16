from FactoryGenerator import FactoryGenerator
from Factory import Factory
import json
from Factory import visibilityStatus


class TestSuite:
    def __init__(self, pathToFactoryRunJSON):
        with open(pathToFactoryRunJSON) as run_log:
            self.factory_run = json.load(run_log)

        with open(self.factory_run['constants']['WORKSTATION_JSON']) as workstations:
            self.workstations = json.load(workstations)

        self.factoryGenerator = FactoryGenerator(workstations)

        '''WSPositions Array -> back to Triplet'''
        self.factorySetting = []
        print(self.factory_run['factorySetting'])
        for i in range(len(self.factory_run['factorySetting'])):
            tmp = self.factory_run['factorySetting'].pop(0)
            self.factorySetting.append(tmp)
        #print(self.factory_run['factorySetting'])

            #open factory_run
            #-> workstationsJSON = file['workStations']
            #-> save constants
            # -> save products
            # -> save workstationPositions

    def runTest(self, products, iterations=0):
        print(self.factorySetting)
        factory = self.factoryGenerator.generateFactory(self.factorySetting,
                                                        products, visibilityStatus.NONE)
        fitness = factory.run()
        print(fitness)

    def plotStats(self):
        # plot with best, worst and mean indiv per generation
        x = range(len(evolutionaryOptimizer.save_best_fitness))
        evolutionaryOptimizer.save_worst_fitness.append(
            evolutionaryOptimizer.save_worst_fitness[len(evolutionaryOptimizer.save_worst_fitness) - 1])
        evolutionaryOptimizer.save_mean.append(
            evolutionaryOptimizer.save_mean[len(evolutionaryOptimizer.save_mean) - 1])
        plt.xlabel('Time')
        plt.ylabel('Fitness')
        plt.title('best vs. worst individuals')
        plt.plot(x, evolutionaryOptimizer.save_best_fitness, label='best', color='g')
        plt.legend()
        plt.show()

        # plot with frequency of best fitness
        ypos = range(len(evolutionaryOptimizer.save_best_frequency))
        plt.plot(ypos, evolutionaryOptimizer.save_best_frequency, color='g')
        plt.ylabel('Frequency')
        plt.xlabel('Time')
        plt.title('number of individuals with same best fitness per generation')
        plt.show()

testSuite = TestSuite("optimizedSettings/factory_run_02.json")
products = [(0, 0, 'DFBFG'), (0, 0, 'FFEFG'), (0, 0, 'EGDBD'), (0, 0, 'EACBD'), (0, 0, 'ECBFE'), (0, 0, 'EEBAD'), (0, 0, 'CAEDF'), (0, 0, 'DCCGF'), (0, 0, 'CCGGF'), (0, 0, 'FAFCF')]
testSuite.runTest(products)
