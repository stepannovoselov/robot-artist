import pytest
import requests
from config import *


@pytest.mark.parametrize("payload, expected_status, expected_keys", [
    ({"username": "john_doe", "email": "john@example.com", "password": "SecurePassword123!"}, 201, ["access_token"]),
    ({"username": "", "email": "john@example.com", "password": "SecurePassword123!"}, 400, ["message"]),
    ({"username": "john_doe", "email": "invalid_email", "password": "SecurePassword123!"}, 400, ["message"])
])
def test_register(payload, expected_status, expected_keys):
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    assert response.status_code == expected_status

    response_json = response.json()
    for key in expected_keys:
        assert key in response_json
