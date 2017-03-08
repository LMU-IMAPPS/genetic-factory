from Factory import visibilityStatus

class Individual:

    def __init__(self, DNA):
        self.DNA = DNA
        self.fitness = None

    def evaluateFitness(self, factoryGenerator, vizType=visibilityStatus.NONE):
        self.fitness = factoryGenerator.generateFactory(self.DNA, vizType).run()

    def getFitness(self):
        return self.fitness

    def mutate(self):
        # TODO Mutate
        return self.DNA
