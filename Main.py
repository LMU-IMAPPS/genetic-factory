from tkinter import Tk
from Factory import visibilityStatus
import sys
import constants
import json
from multiprocessing import Pool
from WorkstationView import WorkstationView
from matplotlib import pyplot as plt

from FactoryGenerator import FactoryGenerator
from ProductsOptimizer import ProductOptimizer
from EvolutionaryOptimizer import EvolutionaryOptimizer

import matplotlib
matplotlib.use("TkAgg")


def optimizePositions():
    pool = Pool(None) # Makes a worker thread for every cpu

    for cycle in range(constants.EVOLUTION_CYCLES):
        '''Init products list for generation'''
        productsGeneration = productOptimizer.getGeneration()  # [[(1,1,"ABAC"),..],[(1,1,"ADC"),..],..]
        productsGenerationFitness = []
        for i in range(constants.LISTS_PER_GENERATION):
            productsGenerationFitness.append(0)

        '''Evaluation'''
        individuals = pool.map(evaluate, map(lambda i: (i, productsGeneration, productsGenerationFitness), evolutionaryOptimizer.getIndividuals()))
        evolutionaryOptimizer.setIndividuals(individuals)

        productOptimizer.evaluateGeneration()
        evolutionaryOptimizer.evaluateIndividuals(factoryGenerator)

        ''' Draw just Workstations'''
        if constants.DRAW_EVERY_CYCLE:
            if cycle == 0:
                viewRoot = Tk()
                view = WorkstationView(viewRoot, evolutionaryOptimizer.theBest, constants.FIELD_SIZE, constants.FIELD_SIZE)
                viewRoot.geometry("1000x600+300+50")
            else:
                view.nextTimeStep(evolutionaryOptimizer.theBest)
                view.update()

        '''See whats going on in the console'''
        percentage = round(cycle / constants.EVOLUTION_CYCLES * 100)
        bar = "[" + "=" * round(percentage / 2) + "-" * round(50 - (percentage / 2)) + "]"
        sys.stdout.write("Progress: \r%d%% Done \t %s \tFittest right now at a level of %i" % (
            percentage, bar, evolutionaryOptimizer.getIndividuals()[0].fitness))
        sys.stdout.flush()

    evolutionaryOptimizer.save_best_fitness.append(evolutionaryOptimizer.theBest.fitness)
    the_best_products = productOptimizer.getGeneration()

    '''Show off with best Factory'''
    theBestPositions = evolutionaryOptimizer.theBest.DNA
    # TODO from Products Optimization
    theBestFactory = factoryGenerator.generateFactory(theBestPositions, visibilityStatus.ALL,
                                                      the_best_products[0].DNA)
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
    print(the_best_products[0].DNA)


def evaluate(inputTupel):
    individual = inputTupel[0]
    productsGeneration = inputTupel[1]
    productsGenerationFitness = inputTupel[2]
    fitness = 0
    for evilProductIndex in range(constants.LISTS_PER_GENERATION):
        # todo Random select productList from productsGeneration
        # print(productsGeneration[evilProductIndex])
        singleFitness = individual.evaluateFitness(factoryGenerator, productsGeneration[evilProductIndex].DNA)
        fitness += singleFitness
        # set product list fitness in productsGenerationFitness
        productsGenerationFitness[evilProductIndex] += singleFitness
    fitness = round(fitness / len(productsGeneration))
    individual.setFitness(fitness)
    for i in range(constants.LISTS_PER_GENERATION):
        productsGenerationFitness[i] /= constants.POPULATION_SIZE
        productsGeneration[i].setFitness(productsGenerationFitness[i])

    return individual


def drawPlots():
    # plot with best, worst and mean indiv per generation
    x = range(len(evolutionaryOptimizer.save_best_fitness))
    save_worst_fitness.append(save_worst_fitness[len(save_worst_fitness) - 1])
    evolutionaryOptimizer.save_mean.append(evolutionaryOptimizer.save_mean[len(evolutionaryOptimizer.save_mean) - 1])
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




if __name__ == '__main__':
    with open(constants.WORKSTATION_JSON) as jsonFile:
        workstationsJson = json.load(jsonFile)

    save_best_fitness = []
    save_worst_fitness = []

    factoryGenerator = FactoryGenerator(workstationsJson)
    evolutionaryOptimizer = EvolutionaryOptimizer(factoryGenerator)
    productOptimizer = ProductOptimizer(workstationsJson)

    optimizePositions()

    drawPlots()