from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask import Flask
from config import APP_SECRET_KEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['FLASK_PYDANTIC_VALIDATION_ERROR_RAISE'] = True
app.secret_key = APP_SECRET_KEY

db = SQLAlchemy(app)
migrate = Migrate(app, db)
hasher = Bcrypt(app)
