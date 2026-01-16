from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

# load environment variables from the .env file
load_dotenv()

# Ensure OS knows about font MIME types (helps some Windows setups and dev servers)
import mimetypes
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('font/woff', '.woff')

app = Flask(__name__)
app.config.from_object(Config)

# Ensure Flask uses the configured static file cache timeout
app.config.setdefault('SEND_FILE_MAX_AGE_DEFAULT', app.config.get('SEND_FILE_MAX_AGE_DEFAULT'))

# SECRET_KEY and SQLALCHEMY_DATABASE_URI are read from Config (which loads env vars)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)  # Add CSRF protection
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Setup logging
from app.utils.logger import setup_logging
setup_logging(app)

from app.routes.root import *  
from app.routes.user import *
from app.routes.admin import *
# Import model classes to ensure they're registered with SQLAlchemy
from app.models.user import User, Transaction, ProfileChangeLog, Beneficiary, TransactionLimit, Notification

# Optionally auto-create tables on application startup when enabled in config.
if app.config.get('AUTO_CREATE_TABLES', False):
    try:
        with app.app_context():
            db.create_all()
            print('AUTO_CREATE_TABLES is enabled — created missing tables.')
    except Exception as exc:
        # Do not crash the application if table creation fails (e.g., DB missing or permission denied).
        print('AUTO_CREATE_TABLES: failed to create tables (DB may be missing or inaccessible).')
        print('Details:', exc)
        print('If the database does not exist, run: python create_db.py')