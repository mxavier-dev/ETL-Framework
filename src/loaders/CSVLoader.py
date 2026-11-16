import csv
from pathlib import Path

from src.loaders.Loader import Loader

class CSVLoader(Loader):
    def load(self, data:list, destination, schema:dict, write_mode:str):
        destination = destination['path']

        if not Path(destination).is_dir():
            raise ValueError(
                f'The path {destination} is not a directory'
            )

        match write_mode:
            case 'overwrite':
                write_mode = 'w+'
            case 'append':
                write_mode = 'a+'

        with open(
            f'{destination}/transformed_data.csv', write_mode,
            encoding='utf-8', newline=''
        ) as f:
            f.seek(0)
            reader = csv.DictReader(f)
            writer = csv.DictWriter(f, fieldnames=[*schema])
            if list(reader) == []:
                writer.writeheader()
            writer.writerows(data)
