import requests
from config import BASE_URL
from fixtures import user_auth_token
import time


def test_initial_delay(user_auth_token):
    headers = {"Authorization": f"Bearer {user_auth_token}"}
    response = requests.get(f'{BASE_URL}/delay', headers=headers)

    assert response.status_code == 200
    response_json = response.json()
    assert "delay" in response_json
    assert response_json["delay"] == 0


def test_delay_after_painting(user_auth_token):
    headers = {"Authorization": f"Bearer {user_auth_token}"}

    payload = {"x": 5, "y": 5, "color": "white"}
    response = requests.post(f'{BASE_URL}/pixels', json=payload, headers=headers)
    assert response.status_code == 200

    response = requests.get(f'{BASE_URL}/delay', headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert "delay" in response_json
    assert 119000 < response_json["delay"] < 120000


def test_delay_decreases_over_time(user_auth_token):
    headers = {"Authorization": f"Bearer {user_auth_token}"}

    payload = {"x": 10, "y": 10, "color": "black"}
    response = requests.post(f'{BASE_URL}/pixels', json=payload, headers=headers)
    assert response.status_code == 200

    time.sleep(3)

    response = requests.get(f'{BASE_URL}/delay', headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert "delay" in response_json
    assert 110000 <= response_json["delay"] <= 117000
