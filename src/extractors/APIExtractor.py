import requests

from src.extractors.Extractor import Extrator

class APIExtractor(Extrator):
    def extract(self, URL) -> list[dict]:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not isinstance(data, list):
            raise TypeError(
                f'Invalid data type received: expected a list, but received a different data type ({type(data).__name__})'

            )
        if not all(isinstance(d, dict) for d in data):
            raise TypeError(
                'Invalid data type received: expected a list containing only dictionaries.'
            )
        return data
