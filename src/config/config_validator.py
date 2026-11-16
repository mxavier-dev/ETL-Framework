from src.factories.extractor_factory import EXTRACTORS
from src.factories.loader_factory import LOADERS
from pathlib import Path

CONFIG_FIELDS = [
    "extractor",
    "source",
    "schema",
    "loader",
    "destination",
    "write_mode"
]

SUPPORTED_WRITE_MODES = {
    "csv": ['append', 'overwrite'],
    "sqlite": ['append', 'overwrite', 'upsert']
}

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

    if not isinstance(config['destination'], dict):
        raise ValueError(
            f'The destination field has to be a dictionary'
        )

    if config['loader'] == 'csv':
        if config['write_mode'] not in SUPPORTED_WRITE_MODES['csv']:
            raise ValueError(
                f'For loader in csv, write_mode has to be one in {SUPPORTED_WRITE_MODES["csv"]}'
            )

    if config['loader'] == 'sqlite':
        if config['write_mode'] not in SUPPORTED_WRITE_MODES['sqlite']:
            raise ValueError(
                f'For loader in csv, write_mode has to be one in {SUPPORTED_WRITE_MODES["sqlite"]}'
            )

        if not config['destination'].get('table'):
            raise ValueError(
                f'For SQLite loader the "table" field is necessary'
            )

        if not isinstance(config['destination']['table'], str):
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

    if not Path(f'schemas/{config["schema"]}.json').exists():
        raise FileNotFoundError(
            f'Schema "{config["schema"]}" not found'
        )

