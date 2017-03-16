from enum import Enum
import sys
import numpy


class StepResult(Enum):
    MOVED = 1
    BLOCKED = 2
    DONE = 3
    FIRSTDONE = 4


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

    def alt1(self):
        if self == Direction.UP:
            return Direction.UPRIGHT
        if self == Direction.UPRIGHT:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.DOWNRIGHT
        if self == Direction.DOWNRIGHT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.DOWNLEFT
        if self == Direction.DOWNLEFT:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.UPLEFT
        if self == Direction.UPLEFT:
            return Direction.UP

    def alt2(self):
        if self == Direction.UP:
            return Direction.UPLEFT
        if self == Direction.UPRIGHT:
            return Direction.UP
        if self == Direction.RIGHT:
            return Direction.UPRIGHT
        if self == Direction.DOWNRIGHT:
            return Direction.RIGHT
        if self == Direction.DOWN:
            return Direction.DOWNRIGHT
        if self == Direction.DOWNLEFT:
            return Direction.DOWN
        if self == Direction.LEFT:
            return Direction.DOWNLEFT
        if self == Direction.UPLEFT:
            return Direction.LEFT

class Product:

    def run(self, currentFieldStatus):
        self.blockedLastRound = False
        if self.isDone:
            # Done doing nothing
            return StepResult.DONE
        if not self.isInitialized:
            # Trying to move into starting position
            if (self.positionX, self.positionY) not in currentFieldStatus:
                self.findTarget()
                currentFieldStatus.add((self.positionX, self.positionY))
                self.isInitialized = True
                return StepResult.MOVED
            else:
                self.blockedLastRound = True
                return StepResult.BLOCKED
        nextDir = self.findDirection()
        if (self.positionX + nextDir.xAxis(), self.positionY + nextDir.yAxis()) not in currentFieldStatus:
            return self.makeStep(currentFieldStatus, nextDir, StepResult.MOVED)
        else:
            nextDir = nextDir.alt1()
            if self.blockedLastRound and (self.positionX + nextDir.xAxis(), self.positionY + nextDir.yAxis()) not in currentFieldStatus:
                return self.makeStep(currentFieldStatus, nextDir, StepResult.BLOCKED)
        return self.afterStepEvaluation(currentFieldStatus, True, StepResult.MOVED)


    def makeStep(self, currentFieldStatus,nextDir, afterStepBlockResult):
        #moving
        currentFieldStatus.remove((self.positionX, self.positionY))
        self.positionX += nextDir.xAxis()
        self.positionY += nextDir.yAxis()
        currentFieldStatus.add((self.positionX, self.positionY))
        return self.afterStepEvaluation(currentFieldStatus, False, afterStepBlockResult)

    def afterStepEvaluation(self, currentFieldStatus, isDefaultBlocked, afterBlockedStepResult):
        if (self.positionY == self.targetY) & (self.positionX == self.targetX):
            if self.timeAtNextWorkstation == 0:
                self.findTarget()
                if self.isDone:
                    # removing myself from the simulation, when I am done
                    currentFieldStatus.remove((self.positionX, self.positionY))
                    return StepResult.FIRSTDONE
                return StepResult.MOVED
            else:
                self.timeAtNextWorkstation -= 1
                return StepResult.MOVED
        if isDefaultBlocked:
            self.blockedLastRound = True
            return afterBlockedStepResult
        return StepResult.MOVED

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
        self.timeAtNextWorkstation = 0
        self.blockedLastRound = False

    def findTarget(self):
        if len(self.workStationRoute) == 0:
            #no workstations left
            self.isDone = True
            return
        nextTarget = self.workStationRoute.pop(0)
        nextTarget = self.findClosest(self.workStations[nextTarget])
        self.targetX = nextTarget.positionX
        self.targetY = nextTarget.positionY
        self.timeAtNextWorkstation = nextTarget.timeAtWs

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
