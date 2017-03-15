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

    def mutate(self, mutationRate, workstationsJson):
        if np.random.random() < mutationRate:
            p = np.random.randint(0, len(self.DNA))
            i = np.random.randint(0, constants.PRODUCTS_PATH_LENGTH)
            workstationTypeIndex = np.random.randint(len(workstationsJson['workStations']))
            first = self.DNA[p][2][:i]
            change = workstationsJson['workStations'][workstationTypeIndex]['type']
            last = self.DNA[p][2][i+1:]
            self.DNA[p] = (self.DNA[p][0], self.DNA[p][1], first + change + last)
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
