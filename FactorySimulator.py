import json
from pprint import pprint
from Product import Product
from Product import StepResult
from Workstation import Workstation
import sys

class FactorySimulator:
    products = []
    workStations = {}

    currentFieldStatus = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    def generate_products(self, path_to_json):
        with open(path_to_json) as data_file:
            data = json.load(data_file)
            for item in data['products']:
                self.products.append(Product(item['positionX'],item['positionY']))

    def generate_work_stations(self, path_to_json):
        with open(path_to_json) as data_file:
            data = json.load(data_file)
            for item in data['workStations']:
                if not item['type'] in self.workStations:
                    # Add new Workstation type
                    self.workStations.update({item['type']: []})

                # Add New Workstation to List of existing type
                self.workStations[item['type']].append(Workstation(item['type']))

    def __init__(self, path_to_products_json, path_to_workstations_json):
        self.generate_products(path_to_products_json)
        self.generate_work_stations(path_to_workstations_json)
        pprint(self.products)
        pprint(self.workStations)
        pprint(self.workStations.values())

    #def setup(self, position_list):
        # for workstations ... setPosition

    def run(self):
        counter = 0;
        while (True):
            madeChange = False
            isDone = True
            for p in self.products:
                result = p.run()
                if not result == StepResult.BLOCKED:
                    madeChange = True
                if not result == StepResult.DONE:
                    isDone = False
            if isDone:
                return counter
            if not madeChange:
                return sys.maxsize
            counter += 1;


Factory = FactorySimulator('Products.json', 'Workstations.json')
position_list = []
#Factory.setup()

