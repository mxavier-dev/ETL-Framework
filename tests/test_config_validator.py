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
        "source": "schemas/example.csv",
        "schema": "example",
        "loader": "csv",
        "destination": {
            "path": "data"
        },
        "write_mode": "append"

    }
    return config

@pytest.mark.parametrize('field',
                         ('extractor', 'source', 'schema',
                          'loader', 'destination', 'write_mode'))
def test_missing_required_field(valid_config, field):
    config = valid_config
    config.pop(field)

    with pytest.raises(ValueError, match=field):
        validate_config(config)

@pytest.mark.parametrize('data', (None, '', 0, False))
@pytest.mark.parametrize('field',
                         ('extractor', 'source', 'schema',
                          'loader', 'destination', 'write_mode'))
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
    config['destination']['table'] = 'table'

    validate_config(config)

@pytest.mark.parametrize('data',
                         (19, True, [2,1]))
def test_sqlite_loader_with_invalid_table_name(valid_config, data):
    config = valid_config
    config['loader'] = 'sqlite'
    config['destination']['table'] = data

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

@pytest.mark.parametrize('write_mode', ('append', 'overwrite', 'upsert'))
def test_valid_write_mode_for_sql_loader(valid_config, write_mode):
    config = valid_config
    config['loader'] = 'sqlite'
    config['destination']['table'] = 'tables'
    config['write_mode'] = write_mode

    validate_config(config)

@pytest.mark.parametrize('write_mode', ('append', 'overwrite'))
def test_valid_write_mode_for_file_loader(valid_config, write_mode):
    config = valid_config
    config['write_mode'] = write_mode

    validate_config(config)

def test_invalid_write_mode_for_sql_loader(valid_config):
    config = valid_config
    config['loader'] = 'sqlite'
    config['destination']['table'] = 'tables'
    config['write_mode'] = 'invalid_write_mode'

    with pytest.raises(ValueError, match='write_mode has to be one'):
        validate_config(config)

def test_invalid_write_mode_for_file_loader(valid_config):
    config = valid_config
    config['write_mode'] = 'invalid_write_mode'

    with pytest.raises(ValueError, match='write_mode has to be one'):
        validate_config(config)
