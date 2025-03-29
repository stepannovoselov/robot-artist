from flask import Blueprint, jsonify
from flask_pydantic import validate
from werkzeug.exceptions import Unauthorized
from schemas import RegisterUser, AuthUser
from manage import db
from methods import *


auth_bp = Blueprint('Authorization blueprint', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@handle_errors
@validate()
def register_user_handler(body: RegisterUser):
    user = create_user(body)

    return jsonify({
        'access_token': user.access_token
    }), 201


@auth_bp.route('/login', methods=['POST'])
@handle_errors
@validate()
def user_login_handler(body: AuthUser):
    user = login_user(body)

    return jsonify({
        'access_token': user.access_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@handle_errors
@access_token_required(required_status='user')
def login_user_handler(user):
    if not user.access_token:
        raise Unauthorized

    user.access_token = None
    db.session.commit()

    return jsonify({
        'message': 'success'
    }), 200
