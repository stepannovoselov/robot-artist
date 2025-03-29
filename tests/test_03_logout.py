import requests
from config import *


def test_logout():
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "john@example.com",
        "password": "SecurePassword123!"
    })
    assert login_response.status_code == 200
    login_json = login_response.json()
    assert "access_token" in login_json
    token = login_json["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    logout_response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    assert logout_response.status_code == 200
    logout_json = logout_response.json()
    assert "message" in logout_json

    logout_again_response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    assert logout_again_response.status_code == 401
    logout_again_json = logout_again_response.json()
    assert "message" in logout_again_json
