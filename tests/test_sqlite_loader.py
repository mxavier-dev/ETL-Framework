import pytest
import sqlite3
from pathlib import Path

from src.loaders.SQLiteLoader import SQLiteLoader

@pytest.fixture
def db_connection():

    def _db_cursor(path, query):
        path = path['path']
        with sqlite3.connect(f'{path}/data_transformed.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        return result

    return _db_cursor

@pytest.fixture
def valid_data_schema():
    schema = {
        'name': {
            'type': 'str'
        },
        'age': {
            'type': 'int'
        }
    }

    data = [
        {'name': 'some', 'age': 2},
        {'name': 'one', 'age': 5}
    ]

    return data, schema

@pytest.fixture
def path_temp(tmp_path):
    path = tmp_path / 'datas'
    path.mkdir()

    return path

def test_database_is_created(valid_data_schema, path_temp):
    data, schema = valid_data_schema
    path = {
        'path': path_temp,
        'table': 'tables'
    }

    SQLiteLoader().load(data, path, schema, 'append')

    assert Path(f'{path["path"]}/data_transformed.db').exists()

def test_table_is_created(valid_data_schema, path_temp, db_connection):
    data, schema = valid_data_schema
    path = {
        'path': path_temp,
        'table': 'tables'
    }


    SQLiteLoader().load(data, path, schema, 'append')

    result = db_connection(
        path,
        '''
        SELECT name FROM sqlite_master
        WHERE type="table" and name="tables"
        '''
    )

    assert result == [('tables',)]

def test_load_respects_schema_types(valid_data_schema, path_temp, db_connection):
    data, schema = valid_data_schema
    path = {
        'path': path_temp,
        'table': 'tables'
    }

    SQLiteLoader().load(data, path, schema, 'append')

    result = db_connection(path, 'PRAGMA table_info(tables)')

    assert result[0][1:3] == ('name', 'TEXT')
    assert result[1][1:3] == ('age', 'INTEGER')

def test_load_empty_data(valid_data_schema, path_temp, db_connection):
    data, schema = valid_data_schema
    path = {
        'path': path_temp,
        'table': 'tables'
    }

    data = []

    SQLiteLoader().load(data, path, schema, 'append')

    result = db_connection(path, 'SELECT * FROM tables')

    assert result == []

def test_load_preserves_all_rows(valid_data_schema, path_temp, db_connection):
    data, schema = valid_data_schema
    path = {
        'path': path_temp,
        'table': 'tables'
    }

    SQLiteLoader().load(data, path, schema, 'append')

    result = db_connection(path, 'SELECT * FROM tables')

    assert result[0] == ('some', 2)
    assert result[1] == ('one', 5)

def test_load_preserves_null_values(valid_data_schema, path_temp, db_connection):
    data, schema = valid_data_schema
    path = {
        'path': path_temp,
        'table': 'tables'
    }

    data[0]['name'] = None

    SQLiteLoader().load(data, path, schema, 'append')

    result = db_connection(path, 'SELECT * FROM tables WHERE name IS NULL')

    assert None in result[0]

def test_invalid_destination():
    path = {
        'path': 'invalid_path',
        'table': 'tables'
    }
    with pytest.raises(ValueError, match='is not a directory'):
        SQLiteLoader().load([], path, 'schema', 'append')

def test_load_to_file_path(path_temp):
    file = path_temp / 'file.csv'
    path = {
        'path': file,
        'table': 'tables'
    }

    with pytest.raises(ValueError, match='is not a directory'):
        SQLiteLoader().load([], path, 'schema', 'append')
