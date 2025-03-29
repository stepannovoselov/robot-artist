from .auth_bp import auth_bp
from .board_bp import board_bp
from .robot_bp import robot_bp
from .service_bp import service_bp


routes = [auth_bp, board_bp, robot_bp, service_bp]
