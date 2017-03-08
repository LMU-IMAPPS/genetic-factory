from Factory import visibilityStatus
import numpy as np


class Individual:

    def __init__(self, DNA):
        self.DNA = DNA
        self.fitness = None

    def evaluateFitness(self, factoryGenerator, vizType=visibilityStatus.NONE):
        self.fitness = factoryGenerator.generateFactory(self.DNA, vizType).run()

    def getFitness(self):
        return self.fitness

    def mutate(self, mutationRate):
        if np.random.random() < mutationRate:
            #print(self.DNA)
            for i in range(len(self.DNA)):
                wsPositionTmp = self.DNA.pop(0)
                newX = wsPositionTmp[1] + np.random.randint(-1, 1) if wsPositionTmp[1] > 0 else 0
                newY = wsPositionTmp[2] + np.random.randint(-1, 1) if wsPositionTmp[2] > 0 else 0
                self.DNA.append((wsPositionTmp[0], newX, newY))
            # TODO Mutate
            #print(self.DNA)

        return self.DNA
