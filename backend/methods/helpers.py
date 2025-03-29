import jwt
from functools import wraps
from flask import request, jsonify
from flask_pydantic import ValidationError
from werkzeug.exceptions import Forbidden, NotFound, Unauthorized
from exceptions import *
from config import APP_SECRET_KEY
from models import User


def get_bearer_token():
    header = request.headers.get('Authorization', None)

    if header:
        parts = header.split(' ')
        if parts[0].lower() == 'bearer' and len(parts) == 2:
            return parts[1]

    raise IncorrectAuthError


def access_token_required(required_status):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = get_bearer_token()

            try:
                data = jwt.decode(token, APP_SECRET_KEY, algorithms=["HS256"])
                current_user = User.query.filter(User.email == data['email']).first_or_404()
            except:
                raise IncorrectAuthError

            if required_status == 'admin' and current_user.status != 'admin':
                raise Forbidden

            return func(current_user, *args, **kwargs)

        return decorated
    return decorator


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError:
            return jsonify({
                'status': 'error',
                'message': 'Ошибка в данных запроса.'
            }), 400
        except NotUniqueError:
            return jsonify({
                'status': 'error',
                'message': 'Такой email или имя пользователя уже существует.'
            }), 409
        except IncorrectAuthError:
            return jsonify({
                'status': 'error',
                'message': 'Неверный email или пароль.'
            }), 401
        except Forbidden:
            return jsonify({
                'status': 'error',
                'message': 'У вас нет доступа к этой странице.'
            }), 403
        except NotFound:
            return jsonify({
              "status": "error",
              "message": "Объект не найден."
            }), 404
        except Unauthorized:
            return jsonify({
              "status": "error",
              "message": "Некорректные данные для авторизации."
            }), 401
        except Exception as e:
            print(e)
            return jsonify({
                "status": "error",
                "message": "Server error. Please, try again later."
            }), 400

    wrapper.__name__ = func.__name__
    return wrapper
