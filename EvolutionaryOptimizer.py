from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual


def generateIndividual(positionList):
    return Individual(positionList)


def individualSelection(individuals):
    # Sort
    individuals.sort(key=lambda y: y.fitness)
    print(individuals[0].fitness)

    # Return Sublist with best <SELECTION_FACTOR> from Individuals
    return individuals[0: -round(SELECTION_FACTOR*len(individuals))]


def optimizePositions(populationSize, cycles):
    individuals = []
    theBest = None

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

        '''Preserve the best found so far'''
        if theBest is None or individuals[0].fitness < theBest.fitness:
            theBest = individuals.pop(0)

        '''Mutation'''
        for i in range(len(individuals)):
            individual = individuals.pop(0)
            individuals.append(individual.mutate(MUTATION_FACTOR))

        '''Breed theBest'''
        for i in range(BREED_FACTOR):
            individuals.append(theBest.mutatedCopy())


        '''Recombination'''

        '''Fill up with random new'''
        while len(individuals) < populationSize:
            positionList = factoryGenerator.generateRandomWorkstations(FIELD_SIZE)
            individuals.append(generateIndividual(positionList))

    '''Show off with best Factory'''
    theBestPositions = theBest.DNA
    theBestFactory = factoryGenerator.generateFactory(theBestPositions, visibilityStatus.ALL)
    theBestFactory.run()


'''Global Genetic Factors'''
SELECTION_FACTOR = 0.85
MUTATION_FACTOR = 0.2
BREED_FACTOR = 2

POPULATION_SIZE = 100
EVOLUTION_CYCLES = 5000

FIELD_SIZE = 200

factoryGenerator = FactoryGenerator('ProductBig.json', 'WorkstationsBig.json')

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
