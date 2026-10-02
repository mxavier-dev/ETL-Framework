from src.extractors.APIExtractor import APIExtractor
from src.extractors.CSVExtractor import CSVExtractor

EXTRACTORS = {
    "csv": CSVExtractor,
    "api": APIExtractor
}

def create_extractor(extractor_type):
    extractor = EXTRACTORS.get(extractor_type)

    if extractor is None:
        raise ValueError(
            f'Extractor "{extractor_type}" is not supported'
        )

    return extractor()
