from flask import Blueprint, jsonify
from flask_pydantic import validate
from schemas import RobotCommand
from methods import *


robot_bp = Blueprint('robot blueprint', __name__)


@robot_bp.route('/command', methods=['POST'])
@handle_errors
@access_token_required(required_status='admin')
@validate()
def handle_robot_command(user, body: RobotCommand):
    command = body.command
    # TODO: actions
    return {}, 200


@robot_bp.route('/status', methods=['GET'])
@handle_errors
@access_token_required(required_status='admin')
def get_robot_status(user):
    # TODO: actions
    return jsonify({
        'status': ''
    }), 200


