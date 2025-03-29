import pytest
import requests
from config import *


@pytest.mark.parametrize("payload, expected_status, expected_keys", [
    ({"email": "john@example.com", "password": "SecurePassword123!"}, 200, ["access_token"]),
    ({"email": "john@example.com", "password": "WrongPassword"}, 401, ["message"]),
    ({"email": "nonexistent@example.com", "password": "SecurePassword123!"}, 404, ["message"]),
    ({"email": "", "password": "SecurePassword123!"}, 400, ["message"]),
])
def test_login(payload, expected_status, expected_keys):
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    assert response.status_code == expected_status

    response_json = response.json()
    for key in expected_keys:
        assert key in response_json
