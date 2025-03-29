from manage import app
from config import APP_HOST, APP_PORT, APP_DEBUG
from routes import routes


for route in routes:
    app.register_blueprint(route)


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
