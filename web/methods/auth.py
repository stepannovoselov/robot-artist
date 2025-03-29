import jwt
from werkzeug.exceptions import Unauthorized
from models import User
from exceptions import *
from manage import hasher, db
from config import APP_SECRET_KEY


def create_user(user_data):
    user_email = User.query.filter(User.email == user_data.email).first()
    user_username = User.query.filter(User.email == user_data.username).first()
    if user_email or user_username:
        raise NotUniqueError

    user_password_hash = hasher.generate_password_hash(user_data.password)
    access_token = jwt.encode({'email': user_data.email}, APP_SECRET_KEY, algorithm="HS256")
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=user_password_hash,
        access_token=access_token
    )

    db.session.add(user)
    db.session.commit()

    return user


def login_user(user_data):
    user = User.query.filter(User.email == user_data.email).first_or_404()

    if not hasher.check_password_hash(user.password_hash, user_data.password):
        raise Unauthorized

    access_token = jwt.encode({'email': user_data.email}, APP_SECRET_KEY, algorithm="HS256")
    user.access_token = access_token
    db.session.commit()

    return user
