import json

from src.extractors.Extractor import Extrator

class JSONExtractor(Extrator):
    def extract(self, path) -> list[dict]:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise TypeError(
                    f'Invalid JSON structure: expected a list, but received a different data type ({type(data).__name__})'
                )
            if not all(isinstance(d, dict) for d in data):
                raise TypeError(
                    'Invalid JSON structure: expected a list containing only dictionaries.'
                )
            return data
