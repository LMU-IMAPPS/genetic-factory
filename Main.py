import os
from tkinter import Tk
from Factory import visibilityStatus
import sys
import constants
import json
from multiprocessing import Pool
from WorkstationView import WorkstationView

from FactoryGenerator import FactoryGenerator
from ProductsOptimizer import ProductOptimizer
from EvolutionaryOptimizer import EvolutionaryOptimizer

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


def optimizePositions(factoryGenerator):
    pool = Pool(None) # Makes a worker thread for every cpu

    for cycle in range(constants.EVOLUTION_CYCLES):
        '''Init products list for generation'''
        productsGeneration = productOptimizer.getGeneration()  # [[(1,1,"ABAC"),..],[(1,1,"ADC"),..],..]
        productsGenerationFitness = [0] * constants.LISTS_PER_GENERATION

        dataFromMultiprocessing = dataFromMultiprocessing = pool.map(evaluate, map(lambda i: (i, productsGeneration, factoryGenerator), evolutionaryOptimizer.getIndividuals()))
        for dfmIndex in range(len(dataFromMultiprocessing)):
            evolutionaryOptimizer.getIndividuals()[dfmIndex].setFitness(dataFromMultiprocessing[dfmIndex][0])
            for i in range(constants.LISTS_PER_GENERATION):
                productsGenerationFitness[i] += dataFromMultiprocessing[dfmIndex][1][i]


        for i in range(constants.LISTS_PER_GENERATION):
            productsGenerationFitness[i] /= constants.POPULATION_SIZE
            productsGeneration[i].setFitness(productsGenerationFitness[i])
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
        sys.stdout.write("Progress: \r%d%% Done \t %s \tFittest right now at a level of %i" % (percentage, bar, evolutionaryOptimizer.theBest.fitness))
        sys.stdout.flush()

    evolutionaryOptimizer.save_best_fitness.append(evolutionaryOptimizer.theBest.fitness)
    the_best_products = productOptimizer.getGeneration()

    '''Save Best as JSON to /optimizedSettings'''

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
    factoryGenerator = inputTupel[2]
    productsGenerationFitness = []
    fitness = 0
    for evilProductIndex in range(constants.LISTS_PER_GENERATION):
        # todo Random select productList from productsGeneration
        # print(productsGeneration[evilProductIndex])
        singleFitness = individual.evaluateFitness(factoryGenerator, productsGeneration[evilProductIndex].DNA)
        fitness += singleFitness
        # set product list fitness in productsGenerationFitness
        productsGenerationFitness.append(singleFitness)
    fitness = round(fitness / len(productsGeneration))

    return (fitness, productsGenerationFitness)


def drawPlots():
    # plot with best, worst and mean indiv per generation
    x = range(len(evolutionaryOptimizer.save_best_fitness))
    evolutionaryOptimizer.save_worst_fitness.append(evolutionaryOptimizer.save_worst_fitness[len(evolutionaryOptimizer.save_worst_fitness) - 1])
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

    #diversity plot
    ypos = range(len(evolutionaryOptimizer.save_diversity_plot))
    plt.plot(ypos, evolutionaryOptimizer.save_diversity_plot, color='g')
    plt.ylabel('Diversity')
    plt.xlabel('Time')
    plt.title('diversity of best individuals')
    plt.show()



if __name__ == '__main__':
    with open(constants.WORKSTATION_JSON) as jsonFile:
        workstationsJson = json.load(jsonFile)

    factoryGenerator = FactoryGenerator(workstationsJson)
    evolutionaryOptimizer = EvolutionaryOptimizer(factoryGenerator)
    productOptimizer = ProductOptimizer(workstationsJson, factoryGenerator)

    optimizePositions(factoryGenerator)

    drawPlots()