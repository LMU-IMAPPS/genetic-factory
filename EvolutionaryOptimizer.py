from FactoryGenerator import FactoryGenerator
from Factory import visibilityStatus
from Individual import Individual


def generateIndividual(positionList):
    return Individual(positionList)


def individualSelection(individuals):
    subList = []
    # TODO Try \w pointer
    '''Sort'''

    '''Sublist'''

    return subList



def optimizePositions(populationSize, cycles):
    individuals = []

    for i in range(populationSize):
        # TODO randomize (factoryGenerator.randomPositionList)
        positionList = [('A', 3, 10), ('B', 2, 9), ('C', 7, 0), ('A', 6, 6), ('D', 1, 5)]
        vizType = visibilityStatus.NONE
        individuals.append(generateIndividual(positionList))

    for cycle in range(cycles):
        '''Evaluate'''
        for individual in individuals:
            individual.evaluateFitness(factoryGenerator)
            #print(individual.fitness)



        '''Selection'''
        individuals = individualSelection(individuals)

        '''Mutation'''
        for i in range(len(individuals)):
            individual = individuals.pop(0)
            newPositionList = individual.mutate()
            individuals.append(generateIndividual(newPositionList))


            individual.mutate()

        '''Recombination'''

        '''Fill up with random new'''
        while individuals.len() <


factoryGenerator = FactoryGenerator('Products.json', 'Workstations.json')

optimizePositions(5, 1)
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




    ##position_list = [('A', 3, 10), ('B', 2, 9), ('C', 7, 0), ('A', 6, 6), ('D', 1, 5)]
