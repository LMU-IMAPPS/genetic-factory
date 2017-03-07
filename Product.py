from enum import Enum
import sys


class StepResult(Enum):
    MOVED = 1
    BLOCKED = 2
    DONE = 3


class Direction(Enum):
    UP = (0, 1)
    UPRIGHT = (1, 1)
    RIGHT = (1, 0)
    DOWNRIGHT = (1, -1)
    DOWN = (0, -1)
    DOWNLEFT = (-1, -1)
    LEFT = (-1, 0)
    UPLEFT = (-1, 1)
    STAY = (0, 0)

    def xAxis(self):
        return self.value[0]

    def yAxis(self):
        return self.value[1]


class Product:

    def run(self, currentFieldStatus):
        if self.isDone:
            # Done doing nothing
            return StepResult.DONE
        if not self.isInitialized:
            # Trying to move into starting position
            if not currentFieldStatus[self.positionX][self.positionY]:
                self.findTarget()
                currentFieldStatus[self.positionX][self.positionY] = True
                self.isInitialized = True
                return StepResult.MOVED
            else:
                return StepResult.BLOCKED
        nextDir = self.findDirection()
        if not currentFieldStatus[self.positionX + nextDir.xAxis()][self.positionY + nextDir.yAxis()]:
            #moving
            currentFieldStatus[self.positionX][self.positionY] = False
            self.positionX += nextDir.xAxis()
            self.positionY += nextDir.yAxis()
            currentFieldStatus[self.positionX][self.positionY] = True
            if (self.positionY == self.targetY) & (self.positionX == self.targetX):
                self.findTarget()
                if self.isDone:
                    #removing myself from the simulation, when I am done
                    currentFieldStatus[self.positionX][self.positionY] = False
                    return StepResult.DONE
                return StepResult.MOVED
            return StepResult.MOVED
        if (self.positionY == self.targetY) & (self.positionX == self.targetX):
            #should not be used
            self.findTarget()
            if self.isDone:
                currentFieldStatus[self.positionX][self.positionY] = False
                return StepResult.DONE
            return StepResult.MOVED
        return StepResult.BLOCKED

    def reset(self):
        self.positionY = self.iniPostionY
        self.positionX = self.iniPostionX
        self.isDone = False
        self.isInitialized = False
        self.workStationRoute = list(self.iniWorkstationRoute)

    def findDirection(self):
        if self.positionX < self.targetX:
            if self.positionY < self.targetY:
                return Direction.UPRIGHT
            if self.positionY > self.targetY:
                return Direction.DOWNRIGHT
            return Direction.RIGHT
        if self.positionX > self.targetX:
            if self.positionY < self.targetY:
                return Direction.UPLEFT
            if self.positionY > self.targetY:
                return Direction.DOWNLEFT
            return Direction.LEFT
        if self.positionY < self.targetY:
            return Direction.UP
        if self.positionY > self.targetY:
            return Direction.DOWN
        return Direction.STAY

    def __init__(self, positionX, positionY, workStationRoute, workStations):
        self.positionX = positionX
        self.positionY = positionY
        self.iniPostionX = positionX
        self.iniPostionY = positionY
        self.iniWorkstationRoute = list(workStationRoute)
        self.workStationRoute = list(workStationRoute)
        self.workStations = workStations
        self.isInitialized = False
        self.isDone = False
        self.targetX = -1
        self.targetY = -1

    def findTarget(self):
        if len(self.workStationRoute) == 0:
            #no workstations left
            self.isDone = True
            return
        nextTarget = self.workStationRoute.pop(0)
        nextTarget = self.findClosest(self.workStations[nextTarget])
        self.targetX = nextTarget.positionX
        self.targetY = nextTarget.positionY

    def findClosest(self, workStationList):
        closestWorkstion = None
        distance = sys.maxsize
        for station in workStationList:
            newDis = self.calculateDistance(station)
            if newDis < distance:
                distance = newDis
                closestWorkstion = station
        return closestWorkstion

    def calculateDistance(self, station):
        x = station.positionX - self.positionX
        y = station.positionY - self.positionY
        x2 = x * x
        y2 = y * y
        return x2 + y2
