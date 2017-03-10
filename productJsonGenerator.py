import random
import json


def genertateJson(filname, numProducts, baseCourseLength, startingPositions, stations, courseLengthDeviation = 0):
    with open(filname, 'w',buffering=1000, encoding='utf-8', newline='\n') as jsonFile:
        isFirst = True
        jsonFile.write('{\n\"products\":[\n')

        for i in range(0, numProducts):
            if isFirst:
                isFirst = False
            else:
                jsonFile.write(',\n')
            startingPosition = startingPositions[random.randint(1, len(startingPositions)) - 1]
            jsonFile.write('{\"positionX\": ' + str(startingPosition[0]) + ',\n\"positionY\": '+ str(startingPosition[1]) +',\n\"workstationRoute\": \"')
            lastIndex = -1
            for j in range(0, random.randint(baseCourseLength - courseLengthDeviation, baseCourseLength + courseLengthDeviation +1)):
                nextIndex = lastIndex
                while nextIndex == lastIndex:
                    nextIndex = random.randint(1, len(stations)) -1
                jsonFile.write(stations[nextIndex])
                lastIndex = nextIndex

            jsonFile.write('\"\n}')
        jsonFile.write("]\n}")

def generateJsonUsingAllWorkstations(filname, numProducts, baseCourseLength, startingPostitons, stationJson, courseLengthDeviation = 0):
    stations = ""
    with open (stationJson) as wsJson:
        for station in json.load(wsJson)['workStations']:
            stations = stations + station['type']
    genertateJson(filname,numProducts,baseCourseLength,startingPostitons,stations,courseLengthDeviation)


generateJsonUsingAllWorkstations('ProductsMid.json', 16, 6, [(0, 0), (5, 0)], 'WorkstationsMid.json', courseLengthDeviation= 2)

