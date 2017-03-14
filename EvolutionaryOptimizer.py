from tkinter import Tk

from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual
from WorkstationView import WorkstationView
import sys
import numpy
import constants
import matplotlib
import math
from multiprocessing import Process
from multiprocessing import SimpleQueue
from matplotlib import pyplot as plt

def generateIndividual(positionList):
    return Individual(positionList)


def individualSelection(individuals, plottingData):
    # Sort
    individuals.sort(key=lambda y: y.fitness)


    #save values for plots in lists
    save_mean_current = []
    #save indiv with best fitness
    plottingData.save_best_fitness.append(individuals[0].fitness)

    count_frequency = 0
    for indiv in range(len(individuals)):
        #save frequency of iniv with same best frequency
        if individuals[indiv].fitness == individuals[0].fitness:
            count_frequency+=1
        #save all individuals of this generation without blocked ones
        if individuals[len(individuals)-(indiv+1)].fitness < sys.maxsize:
            save_mean_current.append((individuals[len(individuals) - (indiv + 1)].fitness))

    # if all indiv are blocked take sys.maxsize as value
    if plottingData.save_best_fitness[0] == sys.maxsize:
        plottingData.save_worst_fitness.append(sys.maxsize)
        plottingData.save_mean.append(sys.maxsize)
    else:
        # save worst indiv except blocked ones
        plottingData.save_worst_fitness.append(save_mean_current[0])
        # save mean of generation
        mean_value = numpy.mean(save_mean_current)
        plottingData.save_mean.append(mean_value)

    #save frequency of best fitness
    plottingData.save_best_frequency.append(count_frequency)




    # Return Sublist with best <SELECTION_FACTOR> from Individuals
    nextIndividuals = []
    lenIndividuals = len(individuals)
    for i in range(lenIndividuals):
        if pow(i / lenIndividuals, 1 / (constants.SELECTION_FACTOR * 2)) <= numpy.random.random():
            nextIndividuals.append(individuals[i])
    return nextIndividuals


def consoleReport(reportQueue):
    cycles = [0] * constants.CPU_CORES
    bestFitness = sys.maxsize
    while True:
        report = reportQueue.get()
        if report[0] == -42: # poison pill
            return
        cycles[report[0]] = report[1]
        cycle = 0
        for c in cycles:
            cycle += c
        cycle /= constants.CPU_CORES
        if bestFitness > report[2]:
            bestFitness = report[2]
        '''See whats going on in the console'''
        percentage = round(cycle / constants.EVOLUTION_CYCLES * 100)
        bar = "[" + "=" * round(percentage / 2) + "-" * round(50 - (percentage / 2)) + "]"
        sys.stdout.write("Progress: \r%d%% Done \t %s \tFittest right now at a level of %i" % (percentage, bar, bestFitness))
        sys.stdout.flush()


class PlottingData:
    def __init__(self):
        self.save_best_fitness = []
        self.save_worst_fitness =[]
        self.save_mean = []
        self.save_best_frequency = []

    @staticmethod
    def combine(plottingDatas):
        result = PlottingData()
        for i in range(len(plottingDatas[0].save_best_fitness)):
            worst_fitness = -9999
            best_fitness = sys.maxsize
            best_frequency = 0
            mean = 0
            for plottingData in plottingDatas:
                worst_fitness = max(plottingData.save_worst_fitness[i], worst_fitness)
                if plottingData.save_best_fitness[i] < best_fitness:
                    best_fitness = plottingData.save_best_fitness[i]
                    best_frequency = plottingData.save_best_frequency[i]
                if plottingData.save_best_fitness[i] == best_fitness:
                    best_frequency += plottingData.save_best_frequency[i]
                mean += plottingData.save_mean[i]
            mean /= len(plottingDatas)
            result.save_worst_fitness.append(worst_fitness)
            result.save_best_fitness.append(best_fitness)
            result.save_best_frequency.append(best_frequency)
            result.save_mean.append(mean)
        return result



def work(factoryGenerator, interProcessCommunication, id, resultOutput, reportQueue, plottingDataQueue):
    populationSize = constants.POPULATION_SIZE
    individuals = []
    theBest = None
    plottingData = PlottingData()

    for i in range(populationSize):
        positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)

        individuals.append(generateIndividual(positionList))
    for cycle in range(constants.EVOLUTION_CYCLES):
        '''Evaluation'''
        for individual in individuals:
            individual.evaluateFitness(factoryGenerator)

        '''Selection'''
        individuals = individualSelection(individuals, plottingData)

        '''Make a copy of the best individual'''
        theBest = Individual(list(individuals[0].DNA), initalFitness=individuals[0].fitness)

        '''Migration'''
        if cycle % constants.NUMBER_OF_CYCLES_UNTIL_MIGRATION == 0:
            nextIndividuals = []
            emigrants = []
            for individual in individuals:
                if numpy.random.random() >= constants.MIGRATION_FACTOR:
                    nextIndividuals.append(individual)
                else:
                    emigrants.append(individual)
            individuals = nextIndividuals
            individuals.extend(interProcessCommunication.get())
            interProcessCommunication.put(emigrants)
            reportQueue.put((id, cycle, theBest.fitness))

        '''Mutation'''
        diversity = calculateDiversity(individuals)
        mutationlist = []

        for individual in diversity:
            indifit = individual[1].fitness
            indidiv = individual[0] + 1
            mutationfactor = indifit/(indidiv*100000)
            mutationlist.append((mutationfactor,individual[1]))

        mutationlist.sort(key= lambda i: i[0])
        scala = 1/(len(mutationlist)*2)

        half_max_div = round(diversity[len(diversity) - 1][0] / 2)
        median = diversity[round(len(diversity) / 2)][0]

        if (half_max_div >= median):
            factor = 0.75
        else:
            factor = 0.3

        for individual in range(len(mutationlist)-1):
            tempindiv = mutationlist[individual][1]
            scalaproindiv = (individual +1) * scala + 0.5
            mutationf = constants.MUTATION_FACTOR * scalaproindiv
            tempindiv.mutate(mutationf)
            if (diversity[round((len(diversity) - 1) * factor)][0] < mutationlist[individual][0]):
                if (numpy.random.random() < 0.5):
                    tempindiv.mutate_all(mutationf)
                else:
                    tempindiv.mutate(mutationf)
            else:
                if (numpy.random.random() < 0.4):
                    tempindiv.mutate_all(mutationf)
                else:
                    tempindiv.mutate(mutationf)

        # for individual in individuals:
        #    individual.mutate(constants.MUTATION_FACTOR)
        '''Recombination'''
        for i in range(int(constants.RECOMBINATION_FACTOR * populationSize)):
            ancestorsIndex1 = exponetialDistrubution(len(diversity))
            ancestorsIndex2 = len(diversity) - exponetialDistrubution(len(diversity)) - 1
            individuals.append(Individual.recombine(diversity[ancestorsIndex1][1], diversity[ancestorsIndex2][1]))

        '''Reinsert best individual'''
        individuals.append(theBest)

        '''Fill up with random new'''
        while len(individuals) < populationSize:
            positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)
            individuals.append(generateIndividual(positionList))

        ''' Draw just Workstations'''
        if constants.DRAW_EVERY_CYCLE is True:
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
    plottingDataQueue.put(plottingData)


def optimizePositions(factoryGenerator):
    print("Calculating with a Population Size of %d in %d Evolution Cycles in %d Threads..." % (constants.POPULATION_SIZE, constants.EVOLUTION_CYCLES, constants.CPU_CORES))

    result = []
    interProcessCommunication = SimpleQueue()
    interProcessCommunication.put([])
    resultOutput = SimpleQueue()
    reportQueue = SimpleQueue()
    plottingDataQueue = SimpleQueue()
    for i in range(constants.CPU_CORES):
        Process(target=work, args=(factoryGenerator, interProcessCommunication, i, resultOutput, reportQueue, plottingDataQueue)).start()

    Process(target=consoleReport, args=(reportQueue,)).start()
    for i in range(constants.CPU_CORES):
        result.append(resultOutput.get())
    theBest = min(result, key=lambda r: r.fitness)
    reportQueue.put((-42, -42, -42)) # poison pill

    #plottingData.save_best_fitness.append(theBest.fitness)

    '''Show off with best Factory'''
    theBestPositions = theBest.DNA
    theBestFactory = factoryGenerator.generateFactory(theBestPositions, visibilityStatus.ALL)
    theBestFactory.run()
    fieldToPrint = [["☐" for i in range(constants.FIELD_SIZE)] for j in range(constants.FIELD_SIZE)]
    for pos in theBestPositions:
        fieldToPrint[pos[1]][pos[2]] = pos[0]
    sys.stdout.write("+" + "-" * (constants.FIELD_SIZE * 3) + "+\n")
    for i in range(constants.FIELD_SIZE):
        sys.stdout.write("|")
        for j in range(constants.FIELD_SIZE):
            sys.stdout.write(" %s " % fieldToPrint[i][j])
        sys.stdout.write("|\n")
    sys.stdout.write("+" + "-" * (constants.FIELD_SIZE * 3) + "+\n")
    sys.stdout.flush()

    return plottingDataQueue


def calculateDiversity(individuals):
    result = []
    for individual in individuals:
        divergence = diversityTest(individual, individuals)
        result.append((divergence, individual))
    result.sort(key=lambda i: i[0])
    return result


def exponetialDistrubution(max):
    for i in range(max):
        if pow(0.5 * math.e, (i + 1) * (-0.5)) > numpy.random.random():
            return i

    return 0


def diversityTest(individual, individuals):
    result = 0
    result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    #result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    #result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    #result += individual.divergence(individuals[numpy.random.randint(len(individuals))])
    return result

def drawPlots(plottingDataQueue):
    #plot with best, worst and mean indiv per generation
    plottingDatas = []
    for i in range(constants.CPU_CORES):
        plottingDatas.append(plottingDataQueue.get())
    plottingData = PlottingData.combine(plottingDatas)
    x = range(len(plottingData.save_best_fitness))
    plt.xlabel('Time')
    plt.ylabel('Fitness')
    plt.title('best vs. worst individuals')
    plt.plot(x, plottingData.save_best_fitness, label='best', color='g')
    plt.plot(x, plottingData.save_mean, label='mean', color='b')
    plt.plot(x, plottingData.save_worst_fitness, label='worst', color='r')
    plt.legend()
    plt.show()

    #plot with frequency of best fitness
    ypos = range(len(plottingData.save_best_frequency))
    plt.plot(ypos, plottingData.save_best_frequency, color='g')
    plt.ylabel('Frequency')
    plt.xlabel('Time')
    plt.title('number of individuals with same best fitness per generation')
    plt.show()



if __name__ == '__main__':

    matplotlib.use("TkAgg")


    factoryGenerator = FactoryGenerator(constants.PRODUCT_JSON, constants.WORKSTATION_JSON)
    plottingDataQueue = optimizePositions(factoryGenerator)
    drawPlots(plottingDataQueue)