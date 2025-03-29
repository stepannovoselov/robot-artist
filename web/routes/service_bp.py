import time
from flask import jsonify, Blueprint
from manage import db
from config import APP_DEBUG, DRAW_DELAY_MS
from methods import access_token_required, handle_errors


service_bp = Blueprint('service blueprint', __name__)


@service_bp.route('/ping', methods=['GET'])
def ping():
    if APP_DEBUG:
        return jsonify({
            'status': 'ok',
            'message': 'pong!'
        }), 200
    return {}, 404


@service_bp.route('/drop', methods=['POST'])
def drop():
    if APP_DEBUG:
        for table in reversed(db.metadata.sorted_tables):
            db.session.query(table).delete()
        db.session.commit()
        return {}, 200
    return {}, 404


@service_bp.route('/raise', methods=['POST'])
@access_token_required(required_status='user')
def raise_user(user):
    if APP_DEBUG:
        user.status = 'admin'
        db.session.commit()
        return {}, 200
    return {}, 404


@service_bp.route('/delay', methods=['GET'])
@handle_errors
@access_token_required(required_status='user')
def get_user_delay(user):
    if DRAW_DELAY_MS - (time.time() * 1000 - user.delay) > 0:
        delay = DRAW_DELAY_MS - (time.time() * 1000 - user.delay)
    else:
        delay = 0

    return jsonify({
        'delay': delay
    }), 200
