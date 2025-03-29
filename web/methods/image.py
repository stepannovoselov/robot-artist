import cv2
from io import BytesIO
from PIL import Image
import numpy as np
import base64
from pydantic import ValidationError


def get_image(base64_string):
    if not base64_string.startswith("data:image/"):
        raise ValidationError

    base64_data = base64_string.split(",")[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))

    return image


def closest_color(color):
    colors = {
        (0, 0, 0): "black",
        (255, 255, 255): "white",
        (255, 0, 0): "red"
    }
    return colors[min(colors.keys(), key=lambda c: np.linalg.norm(np.array(color) - np.array(c)))]


def calculate_optimal_pixel_size(width, height):
    base_size = min(width, height)
    if base_size > 1000:
        return 50
    elif base_size > 500:
        return 20
    elif base_size > 200:
        return 10
    else:
        return 5


def split_image_into_pixels(image):
    width, height = image.size
    pixel_size = calculate_optimal_pixel_size(width, height)

    image = image.convert("RGB")

    pixels = np.array(image)
    pixel_dict = {}

    for y in range(0, height, pixel_size):
        for x in range(0, width, pixel_size):
            block = pixels[y:y + pixel_size, x:x + pixel_size]
            avg_color = tuple(np.mean(block.reshape(-1, 3), axis=0).astype(int))
            pixel_dict[(x, y)] = closest_color(avg_color)

    return pixel_dict


def base64_to_svg(image):
    img = image.convert("L")

    img_np = np.array(img)

    _, img_bin = cv2.threshold(img_np, 128, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def base64_to_colored_svg(image):
    img = image.convert("L")

    img_np = np.array(img)

    _, img_bin = cv2.threshold(img_np, 128, 255, cv2.THRESH_BINARY)

    contours_black, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Чёрные линии
    contours_red, _ = cv2.findContours(255 - img_bin, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)  # Инверсия для красных линий

    return contours_black, contours_red

