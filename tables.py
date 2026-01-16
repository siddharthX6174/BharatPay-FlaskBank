"""List tables in the configured PostgreSQL database (reads DB_URI)."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()
DB_URI = os.getenv('DB_URI')
if not DB_URI:
    print('Error: DB_URI environment variable is not set. Set it in .env or your environment.')
    raise SystemExit(1)

engine = create_engine(DB_URI)
inspector = inspect(engine)

tables = inspector.get_table_names()
if not tables:
    print('No tables found in the database.')
else:
    for t in tables:
        print(t)