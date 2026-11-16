import requests
import json
import pytest

from src.extractors.APIExtractor import APIExtractor

class FakeResponse:
    def __init__(self, url, status_code, data):
        self.status_code = status_code
        self.data = data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(
                f'HTTP error: status code is {self.status_code}'
            )

    def json(self):
        try:
            return json.loads(self.data)
        except json.JSONDecodeError as e:
            raise requests.exceptions.JSONDecodeError(
                e.msg, e.doc, e.pos
            )

def test_response_return_200(monkeypatch):
    data = '[{"fakedata": true}]'

    monkeypatch.setattr(requests, 'get',
                        lambda url ,**kwargs: FakeResponse(url, 200, data))

    result = APIExtractor().extract('https://api.com')

    assert result == [{"fakedata": True}]

def test_response_return_500(monkeypatch):
    data = '[{"fakedata": true}]'

    monkeypatch.setattr(requests, 'get',
                        lambda url ,**kwargs: FakeResponse(url, 500, data))

    with pytest.raises(requests.HTTPError):
        APIExtractor().extract('https://api.com')

def test_response_return_connection_error(monkeypatch):
    def fake_error(url ,**kwargs):
        raise requests.ConnectionError(
            'Connection Error'
        )

    monkeypatch.setattr(requests, 'get', fake_error)

    with pytest.raises(requests.ConnectionError):
        APIExtractor().extract('https://api.com')

def test_response_return_timeout_error(monkeypatch):
    def fake_error(url ,**kwargs):
        raise requests.Timeout(
            'Timout Error'
        )

    monkeypatch.setattr(requests, 'get', fake_error)

    with pytest.raises(requests.Timeout):
        APIExtractor().extract('https://api.com')

def test_response_return_json_decode_error(monkeypatch):
    data = "<html>Internal server error in HTTP</html>"

    monkeypatch.setattr(requests, 'get',
                        lambda url ,**kwargs: FakeResponse(url, 200, data))

    with pytest.raises(requests.exceptions.JSONDecodeError):
        APIExtractor().extract('https://api.com')

@pytest.mark.parametrize('data',
                         ('[{"id": "25"}, "string"]',
                          '{"id": "25"}',
                          '[1,2,3]',
                          'null'))
def test_invalid_data_type_received(monkeypatch, data):
    monkeypatch.setattr(requests, 'get',
                        lambda url, **kwargs: FakeResponse(url, 200, data))

    with pytest.raises(TypeError, match='Invalid data type received'):
        APIExtractor().extract('https://api.com')
