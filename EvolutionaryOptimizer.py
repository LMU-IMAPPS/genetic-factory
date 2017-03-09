from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual
import sys
import numpy
import constants

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

save_best_fitness= []
save_worst_fitness= []
save_mean = []


def generateIndividual(positionList):
    return Individual(positionList)


def individualSelection(individuals):
    # Sort
    save_mean_current = []
    individuals.sort(key=lambda y: y.fitness)
    save_best_fitness.append(individuals[0].fitness)
    for worst in range(len(individuals)):
        if individuals[len(individuals)-(worst+1)].fitness < sys.maxsize:
            save_mean_current.append((individuals[len(individuals) - (worst + 1)].fitness))
    if save_best_fitness[0] == sys.maxsize:
        save_worst_fitness.append(sys.maxsize)
        save_mean.append(sys.maxsize)

    save_worst_fitness.append(save_mean_current[0])
    mean_value = numpy.mean(save_mean_current)
    save_mean.append(mean_value)

    # print(individuals[0].fitness)

    # Return Sublist with best <SELECTION_FACTOR> from Individuals
    nextIndividuals = []
    lenIndividuals = len(individuals)
    for i in range(lenIndividuals):
        if pow(i / lenIndividuals, 1 / constants.SELECTION_FACTOR) < numpy.random.random():
            nextIndividuals.append(individuals[i])
    return nextIndividuals



def optimizePositions(populationSize, cycles):
    individuals = []
    theBest = None

    for i in range(populationSize):
        positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)
        individuals.append(generateIndividual(positionList))
    print("Calculating with a Population Size of %d in %d Evolution Cycles..." % (constants.POPULATION_SIZE, constants.EVOLUTION_CYCLES))

    for cycle in range(cycles):
        '''Evaluation'''
        for individual in individuals:
            individual.evaluateFitness(factoryGenerator)

        '''Selection'''
        individuals = individualSelection(individuals)

        '''See whats going on in the console'''
        percentage = round(cycle/cycles*100)
        bar = "["+"="*round(percentage/2)+"-"*round(50-(percentage/2))+"]"
        sys.stdout.write("Progress: \r%d%% Done \t %s \tFittest right now at a level of %i" % (percentage, bar, individuals[0].fitness))
        sys.stdout.flush()

        '''Preserve the best found so far'''
        if theBest is None or individuals[0].fitness < theBest.fitness:
            theBest = individuals.pop(0)

        '''Mutation'''
        for individual in individuals:
            individual.mutate(constants.MUTATION_FACTOR)

        '''Breed theBest'''
        for i in range(constants.BREED_FACTOR):
            individuals.append(theBest.mutatedCopy())


        '''Recombination'''
        for i in range(int(constants.RECOMBINATION_FACTOR*populationSize)):
            ancestorIndex1 = 0
            ancestorIndex2 = 0
            while ancestorIndex1 != ancestorIndex2:
                ancestorIndex1 = numpy.random.randint(0, len(individuals))
                ancestorIndex2 = numpy.random.randint(0, len(individuals))
            individuals.append(Individual.recombine(individuals[ancestorIndex1],individuals[ancestorIndex2]))

        '''Fill up with random new'''
        while len(individuals) < populationSize:
            positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)
            individuals.append(generateIndividual(positionList))

    save_best_fitness.append(theBest.fitness)

    print("\n")
    '''Evaluation'''
    for individual in individuals:
        individual.evaluateFitness(factoryGenerator)

    '''Selection'''
    individuals = individualSelection(individuals)

    '''Show off with best Factory'''
    theBestPositions = theBest.DNA
    theBestFactory = factoryGenerator.generateFactory(theBestPositions, visibilityStatus.ALL)
    theBestFactory.run()
    fieldToPrint = [["☐" for i in range(constants.FIELD_SIZE)] for j in range(constants.FIELD_SIZE)]
    for pos in theBestPositions:
        fieldToPrint[pos[1]][pos[2]] = pos[0]
    sys.stdout.write("+"+"-"*(constants.FIELD_SIZE*3)+"+\n")
    for i in range(constants.FIELD_SIZE):
        sys.stdout.write("|")
        for j in range(constants.FIELD_SIZE):
            sys.stdout.write(" %s " % fieldToPrint[i][j])
        sys.stdout.write("|\n")
    sys.stdout.write("+" + "-" * (constants.FIELD_SIZE * 3) + "+\n")
    sys.stdout.flush()





factoryGenerator = FactoryGenerator('Products.json', 'Workstations.json')

optimizePositions(constants.POPULATION_SIZE, constants.EVOLUTION_CYCLES)

x = range(len(save_best_fitness))
save_worst_fitness.append(save_worst_fitness[len(save_worst_fitness)-1])
save_mean.append(save_mean[len(save_mean)-1])
plt.xlabel('Time')
plt.ylabel('Fitness')
plt.title('best vs. worst Individuals')
print(save_worst_fitness[len(save_worst_fitness)-2])

plt.plot(x, save_best_fitness, label ='best', color='g')
plt.plot(x,save_mean, label = 'mean', color='b')
plt.plot(x, save_worst_fitness, label = 'worst', color='r')
plt.legend()
plt.show()