from flask import Blueprint, jsonify, render_template, session, request
from flask_pydantic import validate
from werkzeug.exceptions import Unauthorized
from schemas import RegisterUser, AuthUser
from manage import db
from methods import *


auth_bp = Blueprint('Authorization blueprint', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@handle_errors
@no_access_token
@validate()
def register_user_handler(body: RegisterUser):
    user = create_user(body)

    session['access_token'] = user.access_token

    return jsonify({
        'access_token': user.access_token
    }), 201


@auth_bp.route('/login', methods=['POST'])
@handle_errors
@no_access_token
@validate()
def user_login_handler(body: AuthUser):
    user = login_user(body)

    session['access_token'] = user.access_token

    return jsonify({
        'access_token': user.access_token
    }), 200


@auth_bp.route('/login', methods=['GET'])
@handle_errors
@no_access_token
def get_login_form():
    return render_template('auth.html', current_page=request.path, logged=False)


@auth_bp.route('/register', methods=['GET'])
@handle_errors
@no_access_token
def get_register_form():
    return render_template('register.html', current_page=request.path, logged=False)


@auth_bp.route('/logout', methods=['GET'])
@handle_errors
@access_token_required(required_status='user')
def login_user_handler(user):
    if not user.access_token:
        raise Unauthorized

    user.access_token = None
    db.session.commit()
    session.clear()

    if 'text/html' in str(request.accept_mimetypes):
        return render_template('board.html', current_page=request.path, logged=True)
    return jsonify({
        'message': 'success'
    }), 200
