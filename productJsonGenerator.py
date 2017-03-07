import random


def genertateJson(filname, numProducts, baseCourseLength, startingPositions, stations, courseLengthDeviation = 0):
    with open(filname, 'w',buffering=1000, encoding='utf-8', newline='\n') as json:
        isFirst = True
        json.write('{\n\"products\":[\n')

        for i in range(0, numProducts):
            if isFirst:
                isFirst = False
            else:
                json.write(',\n')
            startingPosition = startingPositions[random.randint(1, len(startingPositions)) - 1]
            json.write('{\"positionX\": ' + str(startingPosition[0]) + ',\n\"positionY\": '+ str(startingPosition[1]) +',\n\"workstationRoute\": \"')
            lastIndex = -1
            for j in range(0, random.randint(baseCourseLength - courseLengthDeviation, baseCourseLength + courseLengthDeviation)):
                nextIndex = lastIndex
                while nextIndex == lastIndex:
                    nextIndex = random.randint(1, len(stations)) -1
                json.write(stations[nextIndex])
                lastIndex = nextIndex

            json.write('\"\n}')
        json.write("]\n}")

genertateJson("test.txt", 25, 3, [(0, 0), (0, 10), (10, 0), (10, 10)], 'ABCDEFGHI', courseLengthDeviation=1)

