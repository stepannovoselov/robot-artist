import requests
from config import BASE_URL
from fixtures import admin_auth_token, user_auth_token
import pytest


@pytest.mark.skip
def test_get_robot_status(admin_auth_token):
    headers = {"Authorization": f"Bearer {admin_auth_token}"}
    response = requests.get(f'{BASE_URL}/status', headers=headers)

    assert response.status_code == 200
    response_json = response.json()
    assert "status" in response_json
    # assert response_json["status"] in ["working", "stopped"]  # TODO
    assert "message" in response_json
    assert isinstance(response_json["message"], str)