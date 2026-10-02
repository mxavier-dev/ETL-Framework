from src.extractors.Extractor import Extrator
import csv

class CSVExtractor(Extrator):
    def extract(self, path):
        data = []
        with open(path, 'r', encoding='utf-8') as arq:
            reader = csv.DictReader(arq)
            for line in reader:
                data.append(line)
        return data
