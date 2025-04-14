import os
import urllib.parse
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (this will load from your .env file)
load_dotenv()


def get_db_engine():
    """
    Creates and returns a SQLAlchemy engine using credentials from the environment.
    Passwords are URL-encoded to handle special characters safely.
    """
    DB_USERNAME = os.getenv("DB_USERNAME")
    # URL-encode the password to handle special characters like '@'
    DB_PASSWORD = urllib.parse.quote(os.getenv("DB_PASSWORD"))
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    return engine
