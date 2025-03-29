from manage import app
from models import User
from config import APP_HOST, APP_PORT, APP_DEBUG
from routes import routes
from flask import render_template, request, jsonify, session


for route in routes:
    app.register_blueprint(route)


@app.route('/', methods=['GET'])
def main():
    if 'text/html' in str(request.accept_mimetypes):
        if 'access_token' in session and User.query.filter(User.access_token == session['access_token']).first():
            return render_template('board.html', current_page=request.path, logged=True)
        return render_template('index.html', current_page=request.path, logged=False)

    return jsonify({
        'status': 'ok'
    }), 200


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
