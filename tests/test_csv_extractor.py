import pytest
import csv

from src.extractors.CSVExtractor import CSVExtractor

@pytest.fixture
def temp_csv_file(tmp_path):

    def _csv_file_creator(header, data):

        csv_dir = tmp_path / 'files'
        csv_dir.mkdir(exist_ok=True)

        csv_file = csv_dir / 'test.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)

        return csv_file

    return _csv_file_creator


def test_valid_csv_file(temp_csv_file):
    header = ['id', 'age']
    data = [
        {'id': '1', 'age': '25'},
        {'id': '2', 'age': 'abc'}
    ]

    csv_file = temp_csv_file(header, data)

    result = CSVExtractor().extract(csv_file)

    assert len(result) == 2
    assert result[0] == data[0]
    assert result[1] == data[1]

def test_csv_file_with_only_header(temp_csv_file):
    header = ['id', 'age']

    csv_file = temp_csv_file(header, [])

    result = CSVExtractor().extract(csv_file)

    assert result == []

def test_csv_file_not_found():

    with pytest.raises(FileNotFoundError, match='not found'):
        CSVExtractor().extract('something.csv')

def test_path_is_a_directory(tmp_path):
    dir = tmp_path / 'dir'
    dir.mkdir()

    with pytest.raises(IsADirectoryError, match='is a directory'):
        CSVExtractor().extract(dir)
