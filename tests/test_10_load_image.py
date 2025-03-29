import pytest
import requests
import base64
from config import BASE_URL
from fixtures import admin_auth_token, sample_image


# TODO
def test_upload_image_success(admin_auth_token, sample_image):
    headers = {"Authorization": f"Bearer {admin_auth_token}"}
    payload = {"image": sample_image.decode('UTF-8'), "mode": "lines"}

    response = requests.post(f'{BASE_URL}/image', json=payload, headers=headers)

    assert response.status_code == 200  # Ожидаем успешную загрузку


# def test_upload_image_unsupported_format(auth_token):
#
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     payload = {"image": "invalid_data", "mode": "pixels"}
#
#     response = requests.post(IMAGE_URL, json=payload, headers=headers)
#
#     assert response.status_code == 400  # Ожидаем ошибку
#     response_json = response.json()
#     assert "message" in response_json
#
#
# def test_upload_image_unauthorized(sample_image):
#
#     payload = {"image": sample_image, "mode": "pixels"}
#     response = requests.post(IMAGE_URL, json=payload)
#
#     assert response.status_code == 401
#     response_json = response.json()
#     assert "message" in response_json
#
#
# def test_image_preview_success(auth_token, sample_image):
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     payload = {"image": sample_image, "mode": "pixels"}
#
#     response = requests.post(PREVIEW_URL, json=payload, headers=headers)
#
#     assert response.status_code == 200
#     response_json = response.json()
#     assert "preview_url" in response_json
#
#
# def test_image_preview_unsupported_format(auth_token):
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     payload = {"image": "invalid_data", "mode": "pixels"}
#
#     response = requests.post(PREVIEW_URL, json=payload, headers=headers)
#
#     assert response.status_code == 400
#     response_json = response.json()
#     assert "message" in response_json
#
#
# def test_image_preview_unauthorized(sample_image):
#     payload = {"image": sample_image, "mode": "pixels"}
#     response = requests.post(PREVIEW_URL, json=payload)
#
#     assert response.status_code == 401
#     response_json = response.json()
#     assert "message" in response_json
