class Workstation:

    def __init__(self, type, positionX, positionY):
        self.type = type
        self.positionX = positionX
        self.positionY = positionY
        self.timeAtWs = -1

    def setTimeAtWs(self, timeAtWs):
        self.timeAtWs = timeAtWs
