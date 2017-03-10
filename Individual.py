from Factory import visibilityStatus
import numpy as np
import constants
import sys

class Individual:
    def __init__(self, DNA):
        self.DNA = DNA
        self.fitness = None
        self.workstationOnDifferentPlacesTest()

    def workstationOnDifferentPlacesTest(self):
        setOfWorkstationPostion = set(map(lambda d: (d[1], d[2]),self.DNA))
        if len(self.DNA) != len(setOfWorkstationPostion):
            self.fitness = sys.maxsize

    def evaluateFitness(self, factoryGenerator, vizType=visibilityStatus.NONE):
        if (self.fitness is None) or (vizType != visibilityStatus.NONE):
            self.fitness = factoryGenerator.generateFactory(self.DNA, vizType).run()

    def getFitness(self):
        return self.fitness

    def mutate(self, mutationRate):
        if np.random.random() < mutationRate:
            self.fitness = None
            for i in range(len(self.DNA)):
                wsPositionTmp = self.DNA[i]
                newX = wsPositionTmp[1] + int(np.random.randint(-1*constants.MUTATION_ZERO_FACTOR, 1*constants.MUTATION_ZERO_FACTOR + 1) / constants.MUTATION_ZERO_FACTOR)
                newY = wsPositionTmp[2] + int(np.random.randint(-2*constants.MUTATION_ZERO_FACTOR, 1*constants.MUTATION_ZERO_FACTOR + 1) / constants.MUTATION_ZERO_FACTOR)
                if newX < 0:
                    newX = 0
                if newY < 0:
                    newY = 0
                if newX >= constants.FIELD_SIZE:
                    newX = constants.FIELD_SIZE - 1
                if newY >= constants.FIELD_SIZE:
                    newY = constants.FIELD_SIZE - 1
                self.DNA[i] = (wsPositionTmp[0], newX, newY)
                self.workstationOnDifferentPlacesTest()
        return self

    @staticmethod
    def recombine(ancestor1, ancestor2):
        ancestor1.DNA.sort(key=lambda individual: individual[0])
        ancestor2.DNA.sort(key=lambda individual: individual[0])
        newIndividual = Individual(list(ancestor1.DNA))
        for i in range(len(newIndividual.DNA)):
            if np.random.random() < 0.5:
                newIndividual.DNA[i] = ancestor2.DNA[i]
        return newIndividual


    def mutatedCopy(self):
        return Individual(list(self.DNA)).mutate(999)
