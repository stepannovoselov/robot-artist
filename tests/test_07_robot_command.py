import requests
from config import BASE_URL
from fixtures import admin_auth_token, user_auth_token


def test_send_command(admin_auth_token):
    payload = {"command": "clear_board"}
    headers = {"Authorization": f"Bearer {admin_auth_token}"}
    response = requests.post(f'{BASE_URL}/command', json=payload, headers=headers)

    assert response.status_code == 200


def test_send_invalid_command(admin_auth_token):
    payload = {"command": "unknown_command"}
    headers = {"Authorization": f"Bearer {admin_auth_token}"}
    response = requests.post(f'{BASE_URL}/command', json=payload, headers=headers)

    assert response.status_code == 400
    response_json = response.json()
    assert "message" in response_json


def test_send_command_without_admin(user_auth_token):
    payload = {"command": "clear_board"}
    headers = {"Authorization": f"Bearer {user_auth_token}"}

    response = requests.post(f'{BASE_URL}/command', json=payload, headers=headers)

    assert response.status_code == 403
    response_json = response.json()
    assert "message" in response_json
