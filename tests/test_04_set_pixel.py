import pytest
import requests
from config import *
from fixtures import user_auth_token


@pytest.mark.parametrize("x, y, color, expected_status", [
    (10, 10, "white", 200),
    (20, 20, "black", 200),
    (PIXELS_X + 1, 10, "white", 400),
    (10, PIXELS_Y + 1, "black", 400),
    (10, 10, "red", 400),
    (-1, 10, "white", 400),
    (10, -1, "black", 400),
])
def test_post_pixel(user_auth_token, x, y, color, expected_status):
    payload = {
        "x": x,
        "y": y,
        "color": color
    }
    headers = {"Authorization": f"Bearer {user_auth_token}"}
    response = requests.post(f"{BASE_URL}/pixels", json=payload, headers=headers)
    assert response.status_code == expected_status

    if expected_status == 200:
        response_json = response.json()
        assert "x" in response_json
        assert "y" in response_json
        assert "color" in response_json
        assert response_json["color"] == color
    elif expected_status == 400:
        response_json = response.json()
        assert "message" in response_json
