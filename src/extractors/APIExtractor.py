from src.extractors.Extractor import Extrator
import requests

class APIExtractor(Extrator):
    def extractor(self, URL):
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        return response.json()
