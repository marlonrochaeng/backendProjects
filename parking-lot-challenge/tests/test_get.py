import pytest
import requests


def test_get_vehicles():
    test = 'http://127.0.0.1:8000/plates/'
    response = requests.get(test)
    assert response.status_code == 200
    response = response.json()
    assert response['vehicles'] == []

    insert_url = 'http://127.0.0.1:8000/register/' + 'AAA-1234'
    response = requests.post(insert_url)
    assert response.status_code == 200

    response = requests.get(test)
    response = response.json()
    assert len(response['vehicles']) == 1
    assert response['vehicles'][0]['id']
    assert response['vehicles'][0]['plate'] == 'AAA-1234'
