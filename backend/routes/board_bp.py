import time
from flask import Blueprint, jsonify
from flask_pydantic import validate
from werkzeug.exceptions import Forbidden
from schemas import SetPixel
from methods import *
from config import DRAW_DELAY_MS


board_bp = Blueprint('board blueprint', __name__, url_prefix='/pixels')


@board_bp.route('/', methods=['GET'])
@handle_errors
@access_token_required(required_status='user')
def get_pixels_on_board(user):
    board = get_board()
    return jsonify(board), 200


@board_bp.route('/', methods=['POST'])
@handle_errors
@access_token_required(required_status='user')
@validate()
def set_pixel_on_board(user, body: SetPixel):
    if time.time() - user.delay < DRAW_DELAY_MS:
        raise Forbidden

    pixel = update_pixel(body.x, body.y, body.color)

    user.delay = time.time()

    return jsonify({
        'x': pixel.x,
        'y': pixel.y,
        'color': pixel.color
    }), 200
