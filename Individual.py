from Factory import visibilityStatus
import numpy as np
from FactoryGenerator import ARRAYSIZE


class Individual:
    def __init__(self, DNA):
        self.DNA = DNA
        self.fitness = None

    def evaluateFitness(self, factoryGenerator, vizType=visibilityStatus.NONE):
        if (self.fitness is None) or (vizType != visibilityStatus.NONE):
            self.fitness = factoryGenerator.generateFactory(self.DNA, vizType).run()

    def getFitness(self):
        return self.fitness

    def mutate(self, mutationRate):
        if np.random.random() < mutationRate:
            self.fitness = None
            # for i in range(len(self.DNA)):
            wsPositionTmp = self.DNA.pop(np.random.randint(0, len(self.DNA)))
            # wsPositionTmp = self.DNA.pop(0)
            newX = wsPositionTmp[1] + np.random.randint(-1, 2)
            newY = wsPositionTmp[2] + np.random.randint(-1, 2)
            if newX < 0:
                newX = 0
            if newY < 0:
                newY = 0
            if newX >= ARRAYSIZE:
                newX = ARRAYSIZE - 1
            if newY >= ARRAYSIZE:
                newY = ARRAYSIZE - 1
            self.DNA.append((wsPositionTmp[0], newX, newY))
        return self

    @staticmethod
    def recombine(ancestor1, ancestor2):
        ancestor1.sort(key=lambda individual: individual[0])
        ancestor2.sort(key=lambda individual: individual[0])
        newIndividual = Individual(list(ancestor1))
        for i in range(newIndividual.DNA):
            if np.random.random() < 0.5:
                newIndividual.DNA[i][1] = ancestor2[i][1]
                newIndividual.DNA[i][2] = ancestor2[i][2]
        return newIndividual

    def mutatedCopy(self):
        return Individual(list(self.DNA)).mutate(999)
