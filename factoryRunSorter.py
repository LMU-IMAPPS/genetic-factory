import json
from os import listdir
from os.path import isfile, join
import os
import Main

onlyfiles = [f for f in listdir('inputFolder') if isfile(join('inputFolder', f))]

for f in onlyfiles:
    with open('inputFolder/' + f) as jsonFile:
        factoryJson = json.load(jsonFile)
    if factoryJson['constants']["COEVOLUTION_ON"]:
        os.rename('inputFolder/'+ f, Main.uniquify('outputFolder/withCoevolution/factory_run.json'))
    else:
        os.rename('inputFolder/'+ f, Main.uniquify('outputFolder/withoutCoevolution/factory_run.json'))

