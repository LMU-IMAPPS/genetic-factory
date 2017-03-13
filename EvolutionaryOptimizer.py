from tkinter import Tk

from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual
import sys
import numpy
import constants
import math
from multiprocessing import Process
from multiprocessing import SimpleQueue

import matplotlib

from WorkstationView import WorkstationView

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

save_best_fitness= []
save_worst_fitness= []
save_mean = []
save_best_frequency=[]


def generateIndividual(positionList):
    return Individual(positionList)


def individualSelection(individuals):
    # Sort
    individuals.sort(key=lambda y: y.fitness)

    """
    #save values for plots in lists
    save_mean_current = []
    #save indiv with best fitness
    save_best_fitness.append(individuals[0].fitness)

    count_frequency = 0
    for indiv in range(len(individuals)):
        #save frequency of iniv with same best frequency
        if individuals[indiv].fitness == individuals[0].fitness:
            count_frequency+=1
        #save all individuals of this generation without blocked ones
        if individuals[len(individuals)-(indiv+1)].fitness < sys.maxsize:
            save_mean_current.append((individuals[len(individuals) - (indiv + 1)].fitness))
    #save frequency of best fitness
    save_best_frequency.append(count_frequency)
    # save worst indiv except blocked ones
    save_worst_fitness.append(save_mean_current[0])
    #save mean of generation
    mean_value = numpy.mean(save_mean_current)
    save_mean.append(mean_value)
    # if all indiv are blocked take sys.maxsize as value
    if save_best_fitness[0] == sys.maxsize:
        save_worst_fitness.append(sys.maxsize)
        save_mean.append(sys.maxsize)
    """

    # Return Sublist with best <SELECTION_FACTOR> from Individuals
    nextIndividuals = []
    lenIndividuals = len(individuals)
    for i in range(lenIndividuals):
        if pow(i / lenIndividuals, 1 / (constants.SELECTION_FACTOR * 2)) <= numpy.random.random():
            nextIndividuals.append(individuals[i])
    return nextIndividuals

def work(factoryGenerator, interProcessCommunication ,id, resultOutput):
    populationSize = constants.POPULATION_SIZE
    individuals = []
    theBest = None

    for i in range(populationSize):
        positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)
        individuals.append(generateIndividual(positionList))
    print("Calculating with a Population Size of %d in %d Evolution Cycles..." % (constants.POPULATION_SIZE, constants.EVOLUTION_CYCLES))

    for cycle in range(constants.EVOLUTION_CYCLES):
        '''Evaluation'''
        for individual in individuals:
            individual.evaluateFitness(factoryGenerator)

        '''Selection'''
        individuals = individualSelection(individuals)

        '''Make a copy of the best individual'''
        theBest = Individual(list(individuals[0].DNA), initalFitness=individuals[0].fitness)

        '''See whats going on in the console'''"""
        percentage = round(cycle/constants.EVOLUTION_CYCLES*100)
        bar = "["+"="*round(percentage/2)+"-"*round(50-(percentage/2))+"]"
        sys.stdout.write("Progress: \r%d%% Done \t %s \tFittest right now at a level of %i" % (percentage, bar, individuals[0].fitness))
        sys.stdout.flush()"""

        '''Migration'''
        if cycle % constants.NUMBER_OF_CYCLES_UNTIL_MIGRATION == 0:
            nextIndividuals = []
            emigrants = []
            for individual in individuals:
                if numpy.random.random() >= constants.MIGRATION_FACTOR:
                    nextIndividuals.append(individual)
                else:
                    emigrants.append(individual)
            immigrants = interProcessCommunication.get()
            while (immigrants[0] == id):
                interProcessCommunication.put(immigrants)
                immigrants= interProcessCommunication.get()
            interProcessCommunication.put((id, emigrants))
            individuals = nextIndividuals
            individuals.extend(immigrants[1])

        '''Mutation'''
        for individual in individuals:
            individual.mutate(constants.MUTATION_FACTOR)

        '''Recombination'''
        divergences = calculateDivergences(individuals)
        for i in range(int(constants.RECOMBINATION_FACTOR*populationSize)):
            ancestorsIndex1 = exponetialDistrubution(len(divergences))
            ancestorsIndex2 = len(divergences) - exponetialDistrubution(len(divergences)) - 1
            individuals.append(Individual.recombine(divergences[ancestorsIndex1][1], divergences[ancestorsIndex2][1]))

        '''Reinsert best individual'''
        individuals.append(theBest)

        '''Fill up with random new'''
        while len(individuals) < populationSize:
            positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)
            individuals.append(generateIndividual(positionList))

        ''' Draw just Workstations'''
        if constants.DRAW_EVERY_CYCLE == True:
            if cycle == 0:
                viewRoot = Tk()
                view = WorkstationView(viewRoot, theBest, constants.FIELD_SIZE, constants.FIELD_SIZE)
                viewRoot.geometry("1000x600+300+50")
            else:
                view.nextTimeStep(theBest)
                view.update()


    for individual in individuals:
        individual.evaluateFitness(factoryGenerator)

    # Sort
    individuals.sort(key=lambda y: y.fitness)
    resultOutput.put(individuals[0])

def optimizePositions(factoryGenerator):
    result = []
    interProcessCommunication = SimpleQueue()
    interProcessCommunication.put((-1, []))
    resultOutput = SimpleQueue()

    for i in range(constants.CPU_CORES):
        Process(target=work, args=(factoryGenerator, interProcessCommunication, i, resultOutput)).start()

    for i in range(constants.CPU_CORES):
        result.append(resultOutput.get())
    theBest = min(result, key= lambda r: r.fitness)

    save_best_fitness.append(theBest.fitness)


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

def calculateDivergences(individuals):
    result = []
    for individual in individuals:
        divergence = divergenceTest(individual, individuals)
        result.append((divergence, individual))
    result.sort(key= lambda i: i[0])
    return result


def exponetialDistrubution(max):
    for i in range(max):
        if pow(0.5 * math.e, (i+1) * (-0.5)) > numpy.random.random():
            return i

    return 0


def divergenceTest(individual, individuals):
    result = 0
    result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    return result

def drawPlots():
    #plot with best, worst and mean indiv per generation
    x = range(len(save_best_fitness))
    save_worst_fitness.append(save_worst_fitness[len(save_worst_fitness) - 1])
    save_mean.append(save_mean[len(save_mean) - 1])
    plt.xlabel('Time')
    plt.ylabel('Fitness')
    plt.title('best vs. worst individuals')
    plt.plot(x, save_best_fitness, label='best', color='g')
    plt.plot(x, save_mean, label='mean', color='b')
    plt.plot(x, save_worst_fitness, label='worst', color='r')
    plt.legend()
    plt.show()

    #plot with frequency of best fitness
    ypos = range(len(save_best_frequency))
    plt.plot(ypos, save_best_frequency, color='g')
    plt.ylabel('Frequency')
    plt.xlabel('Time')
    plt.title('number of individuals with same best fitness per generation')
    plt.show()

if __name__ == '__main__':
    factoryGenerator = FactoryGenerator(constants.PRODUCT_JSON, constants.WORKSTATION_JSON)
    optimizePositions(factoryGenerator)
    # drawPlots()