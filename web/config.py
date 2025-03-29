import os
from dotenv import load_dotenv

load_dotenv()

APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')
APP_DEBUG = bool(os.getenv('APP_DEBUG'))
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')

PIXELS_X = int(os.getenv('PIXELS_X'))
PIXELS_Y = int(os.getenv('PIXELS_Y'))
DRAW_DELAY_MS = int(os.getenv('DRAW_DELAY_MS'))
