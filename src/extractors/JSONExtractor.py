from src.extractors.Extractor import Extrator
import json

class JSONExtractor(Extrator):
    def extract(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

