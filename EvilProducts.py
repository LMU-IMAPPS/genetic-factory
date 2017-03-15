import numpy as np
import constants
import numpy


class WorkstationWaitTimesContainer:
    def __init__(self, additionalWaitTimes):
        self.additionalWaitTimes = dict()
        for awt in additionalWaitTimes:
            if awt in self.additionalWaitTimes:
                self.additionalWaitTimes[awt] += 1
            else:
                self.additionalWaitTimes[awt] = 2

    def get(self, id):
        return dict.get(self.additionalWaitTimes, id, 1)

    def mutate(self, increaseKey):
        decreaseKey = increaseKey
        while decreaseKey == increaseKey:
            decreaseKey = list(self.additionalWaitTimes.keys())[numpy.random.randint(0, len(self.additionalWaitTimes))]

        if self.additionalWaitTimes[decreaseKey] <= 2:
            del self.additionalWaitTimes[decreaseKey]
        else:
            self.additionalWaitTimes[decreaseKey] -= 1

        if increaseKey in self.additionalWaitTimes:
            self.additionalWaitTimes[increaseKey] += 1
        else:
            self.additionalWaitTimes[increaseKey] = 2

    def toList(self):
        result = []
        for k in self.additionalWaitTimes.keys():
            for i in range(self.additionalWaitTimes[k] - 1):
                result.append(k)

        return result

    @staticmethod
    def recombine(wwtcList1, wwtcList2):
        if len(wwtcList1) > len(wwtcList2):
            return WorkstationWaitTimesContainer.recombine(wwtcList2,wwtcList1)
        wwtcList1.sort()
        wwtcList2.sort()
        for i in range(len(wwtcList1)):
            if numpy.random.random() < 0.5:
                wwtcList2[i] = wwtcList1[i]
        return WorkstationWaitTimesContainer(wwtcList2)



class EvilProducts:
    def __init__(self, DNA, additionalWaitTimes, initalFitness = None):
        self.DNA = DNA
        self.fitness = initalFitness
        self.workstationWaitTimes = WorkstationWaitTimesContainer(additionalWaitTimes)

    def getWorkstationWaitTimes(self):
        return self.workstationWaitTimes

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def mutate(self, mutationRate, workstationsJson, workstationTypes):
        if np.random.random() < mutationRate:
            p = np.random.randint(0, len(self.DNA))
            i = np.random.randint(0, constants.PRODUCTS_PATH_LENGTH)
            workstationTypeIndex = np.random.randint(len(workstationsJson['workStations']))
            first = self.DNA[p][2][:i]
            change = workstationsJson['workStations'][workstationTypeIndex]['type']
            last = self.DNA[p][2][i+1:]
            self.DNA[p] = (self.DNA[p][0], self.DNA[p][1], first + change + last)
        if np.random.random() < constants.WAIT_TIMES_MUTATION_FACTOR:
            self.workstationWaitTimes.mutate(workstationTypes[numpy.random.randint(0, len(workstationTypes))])

        return self

    @staticmethod
    def recombine(ancestor1, ancestor2):
        ancestor1WaitTimeList = ancestor1.workstationWaitTimes.toList()
        ancestor2WaitTimeList = ancestor2.workstationWaitTimes.toList()
        new_Evil_Products = EvilProducts(list(ancestor1.DNA), ancestor1WaitTimeList)
        for i in range(len(new_Evil_Products.DNA)):
            if np.random.random() < 0.5:
                new_Evil_Products.setFitness(0)
                new_Evil_Products.DNA[i] = (new_Evil_Products.DNA[i][0], new_Evil_Products.DNA[i][1], ancestor2.DNA[i][2])

        new_Evil_Products.workstationWaitTimes = WorkstationWaitTimesContainer.recombine(ancestor1WaitTimeList,
                                                                                         ancestor2WaitTimeList)
        return new_Evil_Products


