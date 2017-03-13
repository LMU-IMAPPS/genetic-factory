import numpy as np
import constants
import sys


class EvilProducts:
    def __init__(self, DNA, initalFitness = None):
        self.DNA = DNA
        self.fitness = initalFitness

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def mutate(self, mutationRate):
        if np.random.random() < mutationRate:
            i = np.random.randint(0, len(self.DNA))
            self.fitness = None
            wsPositionTmp = self.DNA[i]
            newX = wsPositionTmp[1]
            newY = wsPositionTmp[2]
            while newX == wsPositionTmp[1] and newY == wsPositionTmp[2]:
                newX = wsPositionTmp[1] + np.random.randint(-1, 2)
                newY = wsPositionTmp[2] + np.random.randint(-1, 2)
            if newX < 0:
                newX = 0
            if newY < 0:
                newY = 0
            if newX >= constants.FIELD_SIZE:
                newX = constants.FIELD_SIZE - 1
            if newY >= constants.FIELD_SIZE:
                newY = constants.FIELD_SIZE - 1
            self.DNA[i] = (wsPositionTmp[0], newX, newY)

        return self

    @staticmethod
    def recombine(ancestor1, ancestor2):
        newIndividual = Individual(list(ancestor1.DNA))
        for i in range(len(newIndividual.DNA)):
            if np.random.random() < 0.5:
                newIndividual.DNA[i] = ancestor2.DNA[i]
        return newIndividual

    def diversity(self, other):
        result = 0
        for i in range(len(self.DNA)):
            result += abs(self.DNA[i][1] - other.DNA[i][1])
            result += abs(self.DNA[i][2] - other.DNA[i][2])
        return result

