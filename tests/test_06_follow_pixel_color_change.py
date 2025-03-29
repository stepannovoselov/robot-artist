import requests
from config import *
from fixtures import user_auth_token


def test_change_and_check_pixel_color(user_auth_token):
    payload = {
        "x": 5,
        "y": 5,
        "color": "black"
    }
    headers = {"Authorization": f"Bearer {user_auth_token}"}
    response = requests.post(f"{BASE_URL}/pixels", json=payload, headers=headers)
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/pixels", headers=headers)
    assert response.status_code == 200
    pixels = response.json()
    changed_pixel = next((pixel for pixel in pixels if pixel["x"] == 5 and pixel["y"] == 5), None)
    assert changed_pixel is not None
    assert changed_pixel["color"] == "black"

    payload["color"] = "white"
    response = requests.post(f"{BASE_URL}/pixels", json=payload, headers=headers)
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/pixels", headers=headers)
    assert response.status_code == 200
    pixels = response.json()
    changed_pixel = next((pixel for pixel in pixels if pixel["x"] == 5 and pixel["y"] == 5), None)
    assert changed_pixel is not None
    assert changed_pixel["color"] == "white"
