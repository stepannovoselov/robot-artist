from manage import app
from config import APP_HOST, APP_PORT, APP_DEBUG
from routes import routes
from flask import render_template


for route in routes:
    app.register_blueprint(route)


@app.route('/', methods=['GET'])
def main():
    return render_template(...)


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
