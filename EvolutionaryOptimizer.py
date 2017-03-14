import numpy
import sys
import math

from Individual import Individual
import constants

class EvolutionaryOptimizer:
    save_best_fitness = []
    save_worst_fitness = []
    save_mean = []
    save_best_frequency = []

    def generateIndividual(self, positionList):
        return Individual(positionList)

    def individualSelection(self):
        # Sort
        self.individuals.sort(key=lambda y: y.fitness)

        # save values for plots in lists
        save_mean_current = []
        # save indiv with best fitness
        self.save_best_fitness.append(self.individuals[0].fitness)

        count_frequency = 0
        for indiv in range(len(self.individuals)):
            # save frequency of iniv with same best frequency
            if self.individuals[indiv].fitness == self.individuals[0].fitness:
                count_frequency += 1
            # save all individuals of this generation without blocked ones
            if self.individuals[len(self.individuals) - (indiv + 1)].fitness < sys.maxsize:
                save_mean_current.append(self.individuals[len(self.individuals) - (indiv + 1)].fitness)
        # save frequency of best fitness
        self.save_best_frequency.append(count_frequency)
        # save worst indiv except blocked ones
        self.save_worst_fitness.append(save_mean_current[0])
        # save mean of generation
        mean_value = numpy.mean(save_mean_current)
        self.save_mean.append(mean_value)
        # if all indiv are blocked take sys.maxsize as value
        if self.save_best_fitness[0] == sys.maxsize:
            self.save_worst_fitness.append(sys.maxsize)
            self.save_mean.append(sys.maxsize)

        # Return Sublist with best <SELECTION_FACTOR> from Individuals
        nextIndividuals = []
        lenIndividuals = len(self.individuals)
        for i in range(lenIndividuals):
            if pow(i / lenIndividuals, 1 / (constants.SELECTION_FACTOR * 2)) <= numpy.random.random():
                nextIndividuals.append(self.individuals[i])
        return nextIndividuals

    def evaluateIndividuals(self, factoryGenerator):
        '''Selection'''
        self.individuals = self.individualSelection()

        '''Make a copy of the best individual'''
        self.theBest = Individual(list(self.individuals[0].DNA), initalFitness=self.individuals[0].fitness)

        '''Mutation'''
        for individual in self.individuals:
            individual.mutate(constants.MUTATION_FACTOR)

        '''Recombination'''
        divergences = self.calculateDivergences()
        for i in range(int(constants.RECOMBINATION_FACTOR * constants.POPULATION_SIZE)):
            ancestorsIndex1 = self.exponentialDistribution(len(divergences))
            ancestorsIndex2 = len(divergences) - self.exponentialDistribution(len(divergences)) - 1
            self.individuals.append(Individual.recombine(divergences[ancestorsIndex1][1], divergences[ancestorsIndex2][1]))

        '''Reinsert best individual'''
        self.individuals.append(self.theBest)

        '''Fill up with random new'''
        while len(self.individuals) < constants.POPULATION_SIZE:
            positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)
            self.individuals.append(self.generateIndividual(positionList))

    def __init__(self, factoryGenerator):
        self.theBest = None
        self.individuals = []
        for i in range(constants.POPULATION_SIZE):
            positionList = factoryGenerator.generateRandomWorkstations(constants.FIELD_SIZE - 1)
            self.individuals.append(self.generateIndividual(positionList))
        print("Calculating with a Population Size of %d in %d Evolution Cycles..." % (constants.POPULATION_SIZE, constants.EVOLUTION_CYCLES))

    def getIndividuals(self):
        return self.individuals

    def setIndividuals(self, individuals):
        self.individuals = individuals

    def calculateDivergences(self):
        result = []
        for individual in self.individuals:
            divergence = self.divergenceTest(individual)
            result.append((divergence, individual))
        result.sort(key=lambda i: i[0])
        return result

    def exponentialDistribution(self, max):
        for i in range(max):
            if pow(0.5 * math.e, (i + 1) * (-0.5)) > numpy.random.random():
                return i
        return 0

    def divergenceTest(self, individual):
        result = 0
        result += individual.divergence(self.individuals[numpy.random.randint(len(self.individuals))])
        result += individual.divergence(self.individuals[numpy.random.randint(len(self.individuals))])
        result += individual.divergence(self.individuals[numpy.random.randint(len(self.individuals))])
        return result

