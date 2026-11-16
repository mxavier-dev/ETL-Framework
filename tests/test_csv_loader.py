import pytest
from pathlib import Path
import csv

from src.loaders.CSVLoader import CSVLoader

@pytest.fixture
def read_csv_file():

    def _csv_reader(path):
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for line in reader:
                data.append(line)

        return data

    return _csv_reader

@pytest.fixture
def valid_data_schema():
    schema = {
        'name': {
            'type': str
        },
        'age': {
            'type': int
        }
    }

    data = [
        {'name': 'some', 'age': 25},
        {'name': 'one', 'age': 30},
    ]

    return data, schema

@pytest.fixture
def path_temp(tmp_path):
    path = tmp_path / 'datas'
    path.mkdir(exist_ok=True)

    return path

def test_load_valid_data(valid_data_schema, path_temp):
    data, schema = valid_data_schema
    path = {'path': path_temp}

    CSVLoader().load(data, path, schema, 'overwrite')

    assert Path(f'{path["path"]}/transformed_data.csv').exists() is True

def test_load_empty_data(valid_data_schema, path_temp, read_csv_file):
    data, schema = valid_data_schema
    data = []
    path = {'path': path_temp}

    CSVLoader().load(data, path, schema, 'overwrite')
    loaded = read_csv_file(f'{path["path"]}/transformed_data.csv')

    assert loaded == []

def test_load_preserves_all_rows(valid_data_schema, path_temp, read_csv_file):
    data, schema = valid_data_schema
    path = {'path': path_temp}

    CSVLoader().load(data, path, schema, 'overwrite')
    loaded = read_csv_file(f'{path["path"]}/transformed_data.csv')

    assert len(loaded) == len(data)
    assert loaded[0] == {'name': 'some', 'age': '25'}
    assert loaded[1] == {'name': 'one', 'age': '30'}

def test_load_respects_schema_columns(valid_data_schema, path_temp, read_csv_file):
    data, schema = valid_data_schema
    path = {'path': path_temp}

    CSVLoader().load(data, path, schema, 'overwrite')
    loaded = read_csv_file(f'{path["path"]}/transformed_data.csv')

    assert [*loaded[0]] == [*schema]

def test_load_invalid_destination():
    path = {'path': 'invalid_path'}

    with pytest.raises(ValueError, match='not a directory'):
        CSVLoader().load([], path, 'schema', 'overwrite')

def test_load_overwrites_existing_file(valid_data_schema, path_temp, read_csv_file):
    data, schema = valid_data_schema
    path = {'path': path_temp}

    CSVLoader().load(data, path, schema, 'overwrite')
    loaded1 = read_csv_file(f'{path["path"]}/transformed_data.csv')

    data = []
    CSVLoader().load(data, path, schema, 'overwrite')
    loaded2 = read_csv_file(f'{path["path"]}/transformed_data.csv')

    assert loaded2 != loaded1

def test_load_to_file_path(path_temp):
    file = path_temp / 'file.csv'
    path = {'path': file}

    with pytest.raises(ValueError, match='not a directory'):
        CSVLoader().load([], path, 'schema', 'overwrite')

def test_write_mode_append(valid_data_schema, path_temp, read_csv_file):
    data, schema = valid_data_schema
    path = {'path': path_temp}

    data2 = [
        {'name': 'someone2', 'age': 20}
    ]

    CSVLoader().load(data, path, schema, 'overwrite')
    CSVLoader().load(data2, path, schema, 'append')
    result = read_csv_file(f'{path["path"]}/transformed_data.csv')

    assert result[0] == {'name': 'some', 'age': '25'}
    assert result[1] == {'name': 'one', 'age': '30'}
    assert result[2] == {'name': 'someone2', 'age': '20'}

def test_write_mode_overwrite(valid_data_schema, path_temp, read_csv_file):
    data, schema = valid_data_schema
    path = {'path': path_temp}

    data2 = [
        {'name': 'someone2', 'age': 20}
    ]

    CSVLoader().load(data, path, schema, 'append')
    CSVLoader().load(data2, path, schema, 'overwrite')
    result = read_csv_file(f'{path["path"]}/transformed_data.csv')

    assert result[0] == {'name': 'someone2', 'age': '20'}
