from src.loaders.Loader import Loader
import csv

class CSVLoader(Loader):
    def loader(self, data:list, path:str):
        if not data:
            raise ValueError('The file has to be at least one valid data')

        if path.endswith('/'):
            path += 'data_transformed.csv'
        else:
            path += '/data_transformed.csv'

        keys = list(data[0].keys())
        with open(path, 'w', encoding='utf-8', newline='') as arq:
            writer = csv.DictWriter(arq, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
