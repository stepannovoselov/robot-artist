from dotenv import load_dotenv
import os


load_dotenv()


BASE_URL = os.getenv('BASE_URL')
PIXELS_X = int(os.getenv('PIXELS_X'))
PIXELS_Y = int(os.getenv('PIXELS_Y'))
