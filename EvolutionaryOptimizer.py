from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual


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
        # TODO randomize (factoryGenerator.randomPositionList)
        positionList = factoryGenerator.generateRandomWorkstations(FIELD_SIZE)
        individuals.append(generateIndividual(positionList))

    for cycle in range(cycles):
        print(cycle)
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

    '''Show off with best Factory'''
    theBestPositions = individuals[0].DNA
    theBestFactory = factoryGenerator.generateFactory(theBestPositions, visibilityStatus.ALL)
    theBestFactory.run()


'''Global Genetic Factors'''
SELECTION_FACTOR = 0.5
MUTATION_FACTOR = 0.2

POPULATION_SIZE = 30
EVOLUTION_CYCLES = 50

FIELD_SIZE = 20

factoryGenerator = FactoryGenerator('Products.json', 'Workstations.json')

optimizePositions(POPULATION_SIZE, EVOLUTION_CYCLES)
    #Generate Factories(size)
    # for size: Factory = FactoryCreator('Products.json', 'Workstations.json')

    #set inital positions for all WS is WSs.json

    # while cycles
        # setup
        # run
        # evaluate fitness
            # Factory.getBitString
        # selection
        # mutation & recombination




    #position_list = [('A', 3, 10), ('B', 2, 9), ('C', 7, 0), ('A', 6, 6), ('D', 1, 5)]
