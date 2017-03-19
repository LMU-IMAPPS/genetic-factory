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
    save_diversity_plot = []

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
        else:
            # save worst indiv except blocked ones
            self.save_worst_fitness.append(save_mean_current[0])
            # save mean of generation
            mean_value = numpy.mean(save_mean_current)
            self.save_mean.append(mean_value)

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
        diversity = self.calculateDiversity()
        plotdiversity = list(diversity)
        plotdiversity.sort(key=lambda i: i[1].fitness)
        self.save_diversity_plot.append(plotdiversity[0][0])
        mutationlist = []

        for individual in diversity:
            indifit = individual[1].fitness
            indidiv = individual[0] + 1
            mutationfactor = indifit / (indidiv * 100000)
            mutationlist.append((mutationfactor, individual[1]))

        mutationlist.sort(key=lambda i: i[0])
        scala = 1 / (len(mutationlist) * 2)

        half_max_div = round(diversity[len(diversity) - 1][0] / 2)
        median = diversity[round(len(diversity) / 2)][0]
        factor = 0
        if (half_max_div >= median):
            factor = 0.75
        else:
            factor = 0.3

        for individual in range(len(mutationlist) - 1):
            tempindiv = mutationlist[individual][1]
            scalaproindiv = (individual + 1) * scala + 0.5
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
        for i in range(int(constants.RECOMBINATION_FACTOR * constants.POPULATION_SIZE)):
            ancestorsIndex1 = self.exponentialDistribution(len(diversity))
            ancestorsIndex2 = len(diversity) - self.exponentialDistribution(len(diversity)) - 1
            self.individuals.append(Individual.recombine(diversity[ancestorsIndex1][1], diversity[ancestorsIndex2][1]))

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

    def calculateDiversity(self):
        result = []
        for individual in self.individuals:
            diversity = self.diversityTest(individual)
            result.append((diversity, individual))
        result.sort(key=lambda i: i[0])
        return result

    def exponentialDistribution(self, max):
        for i in range(max):
            if pow(0.5 * math.e, (i + 1) * (-0.5)) > numpy.random.random():
                return i
        return 0

    def diversityTest(self, individual):
        result = 0
        for i in range(constants.DIVERGENCE_COMPARISON_COUNT):
            result += individual.diversity(self.individuals[numpy.random.randint(len(self.individuals))])
        result /= constants.DIVERGENCE_COMPARISON_COUNT
        result /= 2 * constants.FIELD_SIZE
        result /= len(individual.DNA)
        return result
