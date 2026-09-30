from src.loaders.Loader import Loader
import csv
import json

class CSVLoader(Loader):
    def loader(self, data:list, path:str):
        if not data:
            raise ValueError('The file has to be at least one valid data')

        path += 'data_transformed.csv' if path.endswith('/') else '/data_transformed.csv'

        with open('schemas/user.json', 'r', encoding='utf-8') as arq:
            schema = json.load(arq)
            keys = list(schema.keys())

        with open(path, 'w', encoding='utf-8', newline='') as arq:
            writer = csv.DictWriter(arq, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
