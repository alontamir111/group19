import os
from dotenv import load_dotenv
load_dotenv()

# App environment configurations
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG = os.environ.get('DEBUG', 'TRUE') == 'TRUE'
FLASK_RUN_HOST = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
FLASK_RUN_PORT = int(os.environ.get('FLASK_RUN_PORT', 5000))

# Secret key setting for Flask sessions
SECRET_KEY = os.environ.get('SECRET_KEY', b'+\xcb\x0f\xa0\x02\x12\xd8\x16\xd4w\xb8i\xac\xd0?I')

# MongoDB URI configuration
DB_URI = os.environ.get('DB_URI', 'mongodb://localhost:27017/yoga_spot_db')