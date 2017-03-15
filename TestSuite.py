from FactoryGenerator import FactoryGenerator
from Factory import Factory

class TestSuite:
    def __init__(self, pathToFactoryRunJSON):
        #open factory_run
            #-> workstationsJSON = file['workStations']
            #-> save constants
            # -> save products
            # -> save workstationPositions
        self.factoryGenerator = FactoryGenerator(workstationsJSON)

    def runTest(self, products, iterations):
        factory = factoryGenerator.generateFactory()
        factory.run()

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
