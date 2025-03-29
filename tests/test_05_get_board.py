import requests
from config import *
from fixtures import user_auth_token


def test_get_pixels(user_auth_token):
    headers = {"Authorization": f"Bearer {user_auth_token}"}

    response = requests.get(f"{BASE_URL}/pixels", headers=headers)
    assert response.status_code == 200

    response_json = response.json()
    assert isinstance(response_json, list)

    assert len(response_json) == PIXELS_Y * PIXELS_X

    for pixel in response_json:
        assert "x" in pixel
        assert "y" in pixel
        assert "color" in pixel
        assert isinstance(pixel["x"], int)
        assert isinstance(pixel["y"], int)
        assert pixel["color"] in ["white", "black", 'red']

