import time
from flask import Blueprint, jsonify
from flask_pydantic import validate
from werkzeug.exceptions import Forbidden
from schemas import LoadImage
from methods import *
from config import DRAW_DELAY_MS
from manage import db


images_bp = Blueprint('images blueprint', __name__, url_prefix='/image')


@images_bp.route('/', methods=['POST'])
@handle_errors
@access_token_required(required_status='admin')
@validate()
def load_image(user, body: LoadImage):
    image = get_image(body.image)
    if body.mode == 'pixels':
        image_dict = split_image_into_pixels(image)
    else:
        strokes = base64_to_colored_svg(image)

    # TODO: actions

    return jsonify({}), 200

