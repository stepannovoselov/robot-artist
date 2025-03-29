from models import PixelField
from manage import db, redis_client
from config import PIXELS_X, PIXELS_Y


def update_pixel(x, y, color):
    pixel = PixelField(x=x, y=y, color=color)

    db.session.merge(pixel)
    db.session.commit()

    redis_client.rpush("command_queue", f"{x},{y},{color}")

    return pixel


def get_board():
    pixels = PixelField.query.filter(
        PixelField.x.in_(range(PIXELS_X)),
        PixelField.y.in_(range(PIXELS_Y))
    ).all()

    pixel_dict = {(pixel.x, pixel.y): pixel.color for pixel in pixels}

    board = [
        {
            'x': x,
            'y': y,
            'color': pixel_dict.get((x, y), 'white')
        }
        for x in range(PIXELS_X)
        for y in range(PIXELS_Y)
    ]

    return board
