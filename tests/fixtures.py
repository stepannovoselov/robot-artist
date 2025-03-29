from faker import Faker
import pytest
from uuid import uuid4
import requests
from config import BASE_URL
from images_config import base64_str
import base64


faker = Faker(locale='ru_RU')


@pytest.fixture()
def user_auth_token():
    username = faker.user_name() + faker.user_name() + faker.user_name() + faker.user_name()
    email = faker.email()
    password = str(uuid4())

    reg_payload = {
        'username': username,
        'email': email,
        'password': password
    }
    requests.post(f"{BASE_URL}/auth/register", json=reg_payload)

    login_payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_auth_token():
    username = faker.user_name()
    email = faker.email()
    password = str(uuid4())

    reg_payload = {
        'username': username,
        'email': email,
        'password': password
    }
    requests.post(f"{BASE_URL}/auth/register", json=reg_payload)

    login_payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f'{BASE_URL}/raise', headers=headers)
    assert response.status_code == 200

    return token


@pytest.fixture
def sample_image():
    return base64_str
