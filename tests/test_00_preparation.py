import requests
from config import *


def test_ping():
    response = requests.get(f"{BASE_URL}/ping")
    assert response.status_code == 200


def test_drop():
    response = requests.post(f"{BASE_URL}/drop")
    assert response.status_code == 200


def test_default():
    response = requests.get(f"{BASE_URL}")
    assert response.status_code == 200

