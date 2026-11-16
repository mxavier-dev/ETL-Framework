import json
import pytest

from src.pipeline import Pipeline

@pytest.fixture
def fake_config_schema(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    schema_dir = tmp_path / 'schemas'
    schema_dir.mkdir()

    schema_file = schema_dir / 'schema.json'
    schema_file.write_text(
        json.dumps({
            'id': {'type': 'int'},
            'age': {'type': 'int'}
        }), encoding='utf-8'
    )

    config = {
                "extractor": "csv",
                "source": "test.csv",
                "schema": "schema",
                "loader": "csv",
                "destination": {
                    "path": "data"
                },
                "write_mode": "append"
            }


    config_dir = tmp_path / 'configs'
    config_dir.mkdir()

    config_file = config_dir / 'config_file.json'
    config_file.write_text(
        json.dumps(config),
        encoding='utf-8'
    )

    return config_file


def test_complete_pipeline(monkeypatch, fake_config_schema):
    receive_data = {}
    def fake_extractor(source):
        receive_data['source'] = source
        return [
            {'id': '1', 'age': '20'},
            {'id': '2', 'age': 'abc'}
        ]

    def fake_loader(data, destination, schema, write_mode):
        receive_data['data'] = data
        receive_data['destination'] = destination
        receive_data['schema'] = schema
        receive_data['write_mode'] = write_mode


    pipeline = Pipeline(fake_config_schema)
    monkeypatch.setattr(pipeline.extractor, 'extract', fake_extractor)
    monkeypatch.setattr(pipeline.loader, 'load', fake_loader)

    pipeline.run()

    assert receive_data['data'][0]['id'] == 1
    assert receive_data['data'][1]['id'] == 2
    assert receive_data['data'][0]['age'] == 20
    assert receive_data['data'][1]['age'] is None
    assert receive_data['source'] == 'test.csv'
    assert receive_data['destination'] == {'path': 'data'}
    assert receive_data['schema'] == {'id': {'type': 'int'}, 'age': {'type': 'int'}}
