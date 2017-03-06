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


class Product:

    def run(self, currentFieldStatus):
        if self.isDone:
            return StepResult.DONE
        if not self.isInitalized:
            if not currentFieldStatus[self.positionX][self.positionY]:
                currentFieldStatus[self.positionX][self.positionY] = True
                self.isInitalized = True
                return StepResult.MOVED
            else:
                return StepResult.BLOCKED
        nextDir = self.findDirection()
        if not currentFieldStatus[self.positionX + nextDir.first()][self.positionY + nextDir.second()]:
            currentFieldStatus[self.positionX][self.positionY] = False
            self.positionX += nextDir.first()
            self.positionY += nextDir.second()
            currentFieldStatus[self.positionX][self.positionY] = True
            if (self.positionY == self.targetY & self.positionX == self.targetX):
                self.findTarget()
                if (self.isDone):
                    currentFieldStatus[self.positionX][self.positionY] = False
                    return StepResult.DONE

            return StepResult.MOVED
        return StepResult.BLOCKED


    def findDirection(self):
        if (self.positionX < self.targetX):
            if (self.positionY < self.targetY):
                return Direction.UPRIGHT
            if (self.positionY > self.targetY):
                return  Direction.DOWNRIGHT
            return Direction.RIGHT
        if (self.positionX > self.targetX):
            if (self.positionY < self.targetY):
                return Direction.UPLEFT
            if (self.positionY > self.targetY):
                return  Direction.DOWNLEFT
            return Direction.LEFT
        if (self.positionY < self.positionY):
            return Direction.UP
        if (self.positionY > self.positionY):
            return Direction.DOWN

    def __init__(self, positionX, positionY,workStationRoute, workStations):
        self.positionX = positionX
        self.positionY = positionY
        self.workStationRoute = workStationRoute
        self.workStations = workStations
        self.isInitalized = False
        self.isDone = False;

    def findTarget(self):
        if len(self.workStationRoute) == 0:
            self.isDone = True
            return
        nextTarget = self.workStationRoute.pop([0])
        nextTarget = self.findClosest(self.workStations[nextTarget])
        self.targetX = nextTarget.positionX
        self.targetY = nextTarget.positionY


    def findClosest(self, workStationList):
        clostetWorkstion = None
        distance = sys.Maxsize
        for station in workStationList:
            newDis = self.calculateDistance(station)
            if newDis < distance:
                distance = newDis
                clostetWorkstion = station
        return clostetWorkstion

    def calculateDistance(self, station):
        x = station.positionX - self.positionX
        y = station.positionY - self.positionY
        x2 = x * x
        y2 = y * y
        return x2 + y2


    #def nextStep():
        # proceed one field calculated according to routing algorithm
        # update postion to new position
