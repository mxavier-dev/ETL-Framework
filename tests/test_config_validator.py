import json
import pytest

from src.config.config_validator import validate_config

@pytest.fixture
def valid_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    schema_dir = tmp_path / 'schemas'
    schema_dir.mkdir()

    schema_file = schema_dir / 'example.json'
    schema_file.write_text(
        json.dumps({'id': {'type': 'int'}}),
        encoding='utf-8'
    )

    config = {
        "extractor": "csv",
        "source": "data/example.csv",
        "schema": "example",
        "loader": "csv",
        "destination": "data"

    }
    return config

@pytest.mark.parametrize('field',
                         ('extractor', 'source', 'schema',
                          'loader', 'destination'))
def test_missing_required_field(valid_config, field):
    config = valid_config
    config.pop(field)

    with pytest.raises(ValueError, match=field):
        validate_config(config)

@pytest.mark.parametrize('data', (None, '', 0, False))
@pytest.mark.parametrize('field',
                         ('extractor', 'source', 'schema',
                          'loader', 'destination'))
def test_missing_required_data(valid_config, field, data):
    config = valid_config
    config[field] = data

    with pytest.raises(ValueError, match=field):
        validate_config(config)

def test_unsupported_extractor(valid_config):
    config = valid_config
    config['extractor'] = 'xml'

    with pytest.raises(ValueError, match='Unsupported extractor'):
        validate_config(config)

def test_unsupported_loader(valid_config):
    config = valid_config
    config['loader'] = 'mongodb'

    with pytest.raises(ValueError, match='Unsupported loader'):
        validate_config(config)

def test_sqlite_loader_required_missing_field_table(valid_config):
    config = valid_config
    config['loader'] = 'sqlite'

    with pytest.raises(ValueError, match='table'):
        validate_config(config)

def test_sqlite_loader_with_valid_table_name(valid_config):
    config = valid_config
    config['loader'] = 'sqlite'
    config['table'] = 'table'

    validate_config(config)

@pytest.mark.parametrize('data',
                         (19, True, [2,1]))
def test_sqlite_loader_with_invalid_table_name(valid_config, data):
    config = valid_config
    config['loader'] = 'sqlite'
    config['table'] = data

    with pytest.raises(ValueError, match='string'):
        validate_config(config)

def test_schema_file_not_found(valid_config):
    config = valid_config
    config['schema'] = 'nonexistent'

    with pytest.raises(FileNotFoundError, match='Schema'):
        validate_config(config)

@pytest.mark.parametrize('data', (True, False))
def test_valid_remove_duplicate_field(valid_config, data):
    config = valid_config
    config['remove_duplicates'] = data

    validate_config(config)

@pytest.mark.parametrize('data', ('true', 'false', 1, 0, None))
def test_invalid_remove_duplicate_field(valid_config, data):
    config = valid_config
    config['remove_duplicates'] = data

    with pytest.raises(ValueError, match='remove_duplicates'):
        validate_config(config)
