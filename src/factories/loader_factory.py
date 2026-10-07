from src.loaders.CSVLoader import CSVLoader
from src.loaders.SQLiteLoader import SQLiteLoader

LOADERS = {
    "csv": CSVLoader,
    'sqlite': SQLiteLoader
}

def create_loader(loader_type):
    loader = LOADERS.get(loader_type)

    if loader is None:
        raise ValueError(
            f'Loader "{loader_type}" is not supported'
        )

    return loader()
