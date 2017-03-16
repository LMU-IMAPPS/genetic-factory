''' Global Inputs '''
WORKSTATION_JSON = 'WorkstationsMid.json'
EVOLUTION_CYCLES = 200
FIELD_SIZE = 20
DRAW_EVERY_CYCLE = False
SHOW_PRODUCT_PATH = False

''' Evolutionary Optimizer Constants '''
POPULATION_SIZE = 20
SELECTION_FACTOR = 0.2  # Linear probability of distribution
MUTATION_FACTOR = 0.4
RECOMBINATION_FACTOR = 0.4
DIVERGENCE_COMPARISON_COUNT = 3

''' Product Optimizer Constants '''
COEVOLUTION_ON = False
PRODUCTS_PER_LIST = 10
PRODUCTS_PATH_LENGTH = 5
LISTS_PER_GENERATION = 5
PRODUCTS_SELECTION_FACTOR= 0.2
PRODUCTS_MUTATION_FACTOR = 0.4
PRODUCTS_RECOMBINATION_FACTOR = 0.2

# DO NOT CHANGE THIS
if not COEVOLUTION_ON:
    LISTS_PER_GENERATION = 1
    PRODUCTS_SELECTION_FACTOR= 1
    PRODUCTS_MUTATION_FACTOR = 0

'''Helper function putting all consts into a dict'''
def getConstantsDict():
    constantNames = ['WORKSTATION_JSON', 'EVOLUTION_CYCLES', 'FIELD_SIZE',
                     'POPULATION_SIZE', 'SELECTION_FACTOR', 'MUTATION_FACTOR',
                     'RECOMBINATION_FACTOR', 'DIVERGENCE_COMPARISON_COUNT', 'COEVOLUTION_ON',
                     'PRODUCTS_PER_LIST', 'PRODUCTS_PATH_LENGTH', 'LISTS_PER_GENERATION', 'PRODUCTS_SELECTION_FACTOR',
                     'PRODUCTS_MUTATION_FACTOR', 'PRODUCTS_RECOMBINATION_FACTOR']
    return dict((name, eval(name)) for name in constantNames)



