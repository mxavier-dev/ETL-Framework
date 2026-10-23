from src.factories.extractor_factory import EXTRACTORS
from src.factories.loader_factory import LOADERS
import os

CONFIG_FIELDS = [
    "extractor",
    "source",
    "schema",
    "loader",
    "destination"
]

def validate_config(config):
    for field in CONFIG_FIELDS:
        if field not in config:
            raise ValueError(
                f'The configuration file is missing field "{field}"'
            )

        if not config[field]:
            raise ValueError(
                f'The configuration field "{field}" cannot be empty'
            )

    if config['loader'] == 'sqlite':
        if not config.get('table'):
            raise ValueError(
                f'For SQLite loader the "table" field is necessary'
            )

        if not isinstance(config['table'], str):
            raise ValueError(
                f"The table field has to be a string"
            )

    if config['extractor'] not in EXTRACTORS:
        raise ValueError(
            f'Unsupported extractor "{config["extractor"]}"'
        )

    if config['loader'] not in LOADERS:
        raise ValueError(
            f'Unsupported loader "{config["loader"]}"'
        )

    if 'remove_duplicates' in config:
        if not isinstance(config['remove_duplicates'], bool):
            raise ValueError(
                f'The configuration field "remove_duplicates" has to be boolean (true or false)'
            )

    if not os.path.exists(f'schemas/{config["schema"]}.json'):
        raise FileNotFoundError(
            f'Schema "{config["schema"]}" not found'
        )

