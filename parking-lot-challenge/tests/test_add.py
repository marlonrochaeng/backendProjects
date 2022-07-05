import pytest
import requests

@pytest.mark.parametrize(
    "test_input, expected, status_code",
    [
        ("AAA-1234", "Vehicle AAA-1234 registered at", 200),
        ("AAA-1234", "Vehicle AAA-1234 is already parked", 403),
        ("AAA-1", "Vehicle AAA-1 does not have a valid plate", 403),
        ("AA-1234", "Vehicle AA-1234 does not have a valid plate", 403)
    ],
)
def test_add(test_input, expected, status_code):
    test_url = 'http://127.0.0.1:8000/register/' + test_input
    response = requests.post(test_url)
    assert response.status_code == status_code

    response = response.json()
    assert expected in response['message']
