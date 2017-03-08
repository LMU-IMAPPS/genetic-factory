from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual
import sys


def generateIndividual(positionList):
    return Individual(positionList)


def individualSelection(individuals):
    # Sort
    individuals.sort(key=lambda y: y.fitness)
    # print(individuals[0].fitness)

    # Return Sublist with best <SELECTION_FACTOR> from Individuals
    return individuals[0: -round(SELECTION_FACTOR*len(individuals))]


def optimizePositions(populationSize, cycles):
    individuals = []
    theBest = None

    for i in range(populationSize):
        positionList = factoryGenerator.generateRandomWorkstations(FIELD_SIZE)
        individuals.append(generateIndividual(positionList))
    print("Calculating with a Population Size of %d in %d Evolution Cycles..." % (POPULATION_SIZE, EVOLUTION_CYCLES))

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
            individual.mutate(MUTATION_FACTOR)

        '''Breed theBest'''
        for i in range(BREED_FACTOR):
            individuals.append(theBest.mutatedCopy())

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
    theBestPositions = theBest.DNA
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
SELECTION_FACTOR = 0.85
MUTATION_FACTOR = 0.2
BREED_FACTOR = 1

POPULATION_SIZE = 10
EVOLUTION_CYCLES = 50

FIELD_SIZE = 50

factoryGenerator = FactoryGenerator('ProductBig.json', 'WorkstationsBig.json')

optimizePositions(POPULATION_SIZE, EVOLUTION_CYCLES)
