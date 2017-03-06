class Workstation:
    type = ''
    positionX = -1
    positionY = -1

    def __init__(self, type):
        self.type = type

    def setPosition(self, positionX, positionY):
        self.positionX = positionX
        self.positionY = positionY