from Factory import visibilityStatus
import numpy as np
from FactoryGenerator import ARRAYSIZE


class Individual:

    def __init__(self, DNA):
        self.DNA = DNA
        self.fitness = None

    def evaluateFitness(self, factoryGenerator, vizType=visibilityStatus.NONE):
        if (self.fitness is None) or (vizType is not None):
            self.fitness = factoryGenerator.generateFactory(self.DNA, vizType).run()

    def getFitness(self):
        return self.fitness

    def mutate(self, mutationRate):
        if np.random.random() < mutationRate:
            self.fitness = None
            #print(self.DNA)
            #for i in range(len(self.DNA)):
            wsPositionTmp = self.DNA.pop(np.random.randint(0, len(self.DNA)))
                #wsPositionTmp = self.DNA.pop(0)
            newX = wsPositionTmp[1] + np.random.randint(-1, 1)
            newY = wsPositionTmp[2] + np.random.randint(-1, 1)
            if newX < 0:
                newX = 0
            if newY < 0:
                newY = 0
            if newX >= ARRAYSIZE:
                newX = ARRAYSIZE - 1
            if newY >= ARRAYSIZE:
                newY = ARRAYSIZE - 1
            self.DNA.append((wsPositionTmp[0], newX, newY))
            # TODO Mutate
            #print(self.DNA)

        return self

    def mutatedCopy(self):
        return Individual(list(self.DNA)).mutate(999)