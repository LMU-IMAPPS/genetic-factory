from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual
import sys


def generateIndividual(positionList):
    return Individual(positionList)


def individualSelection(individuals):
    # Sort
    individuals.sort(key=lambda y: y.fitness)

    # Return Sublist with best <SELECTION_FACTOR> from Individuals
    return individuals[0: -round(SELECTION_FACTOR*len(individuals))]


def optimizePositions(populationSize, cycles):
    individuals = []

    for i in range(populationSize):
        positionList = factoryGenerator.generateRandomWorkstations(FIELD_SIZE)
        individuals.append(generateIndividual(positionList))
    print("Calculating with a Population Size of %d in %d Evolution Cycles..." % (POPULATION_SIZE, EVOLUTION_CYCLES))

    for cycle in range(cycles):
        percentage = round(cycle/cycles*100)
        bar = "["+"="*round(percentage/2)+"-"*round(50-(percentage/2))+"]"
        sys.stdout.write("Progress: \r%d%% Done \t %s" % (percentage, bar))
        sys.stdout.flush()

        '''Evaluation'''
        for individual in individuals:
            individual.evaluateFitness(factoryGenerator)

        '''Selection'''
        individuals = individualSelection(individuals)

        '''Mutation'''
        for i in range(len(individuals)):
            individual = individuals.pop(0)
            newPositionList = individual.mutate(MUTATION_FACTOR)
            individuals.append(generateIndividual(newPositionList))

        '''Recombination'''

        '''Fill up with random new'''
        while len(individuals) < populationSize:
            positionList = factoryGenerator.generateRandomWorkstations(FIELD_SIZE)
            individuals.append(generateIndividual(positionList))

    print("\n")
    '''Evaluation'''
    for individual in individuals:
        individual.evaluateFitness(factoryGenerator)

    '''Selection'''
    individuals = individualSelection(individuals)

    '''Show off with best Factory'''
    theBestPositions = individuals[0].DNA
    theBestFactory = factoryGenerator.generateFactory(theBestPositions, visibilityStatus.ALL)
    theBestFactory.run()
    fieldToPrint = [["☐" for i in range(FIELD_SIZE)] for j in range(FIELD_SIZE)]
    for pos in theBestPositions:
        fieldToPrint[pos[1]][pos[2]] = pos[0]
    sys.stdout.write("+"+"-"*(FIELD_SIZE*3)+"+\n")
    for i in range(FIELD_SIZE):
        sys.stdout.write("|")
        for j in range(FIELD_SIZE):
            sys.stdout.write(" %s " % fieldToPrint[i][j])
        sys.stdout.write("|\n")
    sys.stdout.write("+" + "-" * (FIELD_SIZE * 3) + "+\n")
    sys.stdout.flush()


'''Global Genetic Factors'''
SELECTION_FACTOR = 0.5
MUTATION_FACTOR = 0.2

POPULATION_SIZE = 100
EVOLUTION_CYCLES = 200

FIELD_SIZE = 10

factoryGenerator = FactoryGenerator('Products.json', 'Workstations.json')

optimizePositions(POPULATION_SIZE, EVOLUTION_CYCLES)
