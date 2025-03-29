from manage import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_token = db.Column(db.String, nullable=True, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='user', nullable=False)
    delay = db.Column(db.Float, default=0, nullable=False)
