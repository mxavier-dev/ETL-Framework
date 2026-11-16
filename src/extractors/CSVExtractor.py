import csv
from pathlib import Path

from src.extractors.Extractor import Extrator

class CSVExtractor(Extrator):
    def extract(self, path: str) -> list[dict]:
        data = []
        if not Path(path).exists():
            raise FileNotFoundError(
                f'The file in the path "{path}" not found'
            )
        if Path(path).is_dir():
            raise IsADirectoryError(
                f'The path {path} is a directory'
            )

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for line in reader:
                data.append(line)
                
        return data
