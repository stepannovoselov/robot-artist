import jwt
from functools import wraps
from flask import request, jsonify, session, render_template
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

    session_token = session.get('access_token')
    if session_token:
        return session_token

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


def no_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' in session:
            raise Forbidden
        return f(*args, **kwargs)
    return decorated_function


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValidationError:
            code = 400
            message = 'Ошибка в данных запроса.'

            if 'text/html' in str(request.accept_mimetypes):
                return render_template('errors.html', error_code=code, error_message=message, current_page=request.path, logged=False)
            return jsonify({
                'status': 'error',
                "message": message
            }), code

        except NotUniqueError:
            code = 409
            message = 'Почта или имя пользователя уже существуют.'

            if 'text/html' in str(request.accept_mimetypes):
                return render_template('errors.html', error_code=code, error_message=message, current_page=request.path, logged=False)
            return jsonify({
                'status': 'error',
                "message": message
            }), code

        except IncorrectAuthError:
            code = 401
            message = 'Неверный email или пароль.'

            if 'text/html' in str(request.accept_mimetypes):
                return render_template('errors.html', error_code=code, error_message=message, current_page=request.path, logged=False)
            return jsonify({
                'status': 'error',
                "message": message
            }), code

        except Forbidden:
            code = 403
            message = 'У вас нет доступа к этой странице.'

            if 'text/html' in str(request.accept_mimetypes):
                return render_template('errors.html', error_code=code, error_message=message, current_page=request.path, logged=False)
            return jsonify({
                'status': 'error',
                "message": message
            }), code

        except NotFound:
            code = 404
            message = "Объект не найден."

            if 'text/html' in str(request.accept_mimetypes):
                return render_template('errors.html', error_code=code, error_message=message, current_page=request.path, logged=False)
            return jsonify({
              "status": "error",
              "message": message
            }), code

        except Unauthorized:
            code = 401
            message = "Некорректные данные для авторизации."

            if 'text/html' in str(request.accept_mimetypes):
                return render_template('errors.html', error_code=code, error_message=message, current_page=request.path, logged=False)
            return jsonify({
              "status": "error",
              "message": message
            }), code

        except Exception as e:
            code = 400
            message = 'Server error. Please, try again later.'

            if 'text/html' in str(request.accept_mimetypes):
                return render_template('errors.html', error_code=code, error_message=message, current_page=request.path, logged=False)

            print(e)
            return jsonify({
                "status": "error",
                "message": message
            }), code

    wrapper.__name__ = func.__name__
    return wrapper
