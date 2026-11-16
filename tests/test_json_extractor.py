import pytest
import json

from src.extractors.JSONExtractor import JSONExtractor

@pytest.fixture
def temp_json_file(tmp_path):

    def _json_file_creator(data):
        json_dir = tmp_path / 'files'
        json_dir.mkdir(exist_ok=True)

        json_file = json_dir / 'test.json'
        json_file.write_text(
            json.dumps(data),
            encoding='utf-8'
        )

        return json_file

    return _json_file_creator

def test_valid_json_file(temp_json_file):
    data = [
        {'id': '1', 'age': '25'},
        {'id': '2', 'age': '20'},
    ]

    json_file = temp_json_file(data)

    result = JSONExtractor().extract(json_file)

    assert len(result) == 2
    assert result[0] == data[0]
    assert result[1] == data[1]

def test_empty_json_file(temp_json_file):
    data = []

    json_file = temp_json_file(data)

    result = JSONExtractor().extract(json_file)

    assert result == []

def test_invalid_json_file(tmp_path):
    invalid_json = tmp_path / 'invalid_test.json'
    invalid_json.write_text("{'invalid': true}", encoding='utf-8')

    with pytest.raises(json.JSONDecodeError):
        JSONExtractor().extract(invalid_json)

def test_json_file_not_found():

    with pytest.raises(FileNotFoundError):
        JSONExtractor().extract('something.json')

@pytest.mark.parametrize('data',
                         ([{'id': '25'}, 'string'],
                          {'id': '25'},
                          [1,2,3],
                          None))
def test_invalid_type_json_file(temp_json_file, data):
    json_file = temp_json_file(data)

    with pytest.raises(TypeError, match='Invalid JSON structure'):
        JSONExtractor().extract(json_file)
