"""Create PostgreSQL database (if it doesn't exist) and create tables.

It reads the `DB_URI` environment variable. Example `DB_URI`:
    postgresql+psycopg2://user:password@host:5432/database_name

If the target database does not exist, the script will attempt to create it by
connecting to the maintenance DB (usually `postgres`) and issuing
`CREATE DATABASE` (requires appropriate privileges).
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url

load_dotenv()

DB_URI = os.getenv('DB_URI')
if not DB_URI:
    print('Error: DB_URI environment variable is not set.\nPlease set your PostgreSQL URI in the DB_URI env variable or in a .env file.')
    print('Example: postgresql+psycopg2://user:password@host:5432/database_name')
    raise SystemExit(1)

# Parse DB URI and get database name
url = make_url(DB_URI)
db_name = url.database
if not db_name:
    print('Error: DB_URI must include a database name.')
    raise SystemExit(1)

# Create an admin engine that connects to the maintenance DB (postgres)
admin_url = url.set(database='postgres')
admin_engine = create_engine(admin_url)

try:
    with admin_engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f'CREATE DATABASE "{db_name}"'))
        print(f"Database '{db_name}' created.")
except Exception as exc:
    msg = str(exc)
    if 'already exists' in msg or 'duplicate database' in msg.lower():
        print(f"Database '{db_name}' already exists, continuing.")
    else:
        print('Warning: could not create database. It may already exist or you may lack privileges.')
        print('Details:', msg)

# Now create tables via the Flask application's models
from app import app, db
# Import models so SQLAlchemy is aware of them
from app.models.user import User, Transaction  # registers models

with app.app_context():
    db.create_all()
    print('Tables created (if they did not already exist).')