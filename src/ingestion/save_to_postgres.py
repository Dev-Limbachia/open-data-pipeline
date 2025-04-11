import os
from sqlalchemy import create_engine
import urllib.parse
from dotenv import load_dotenv

load_dotenv()


def save_to_postgres(df, table_name):
    """
    Save the stock data DataFrame to PostgreSQL.
    """
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = urllib.parse.quote(os.getenv("DB_PASSWORD"))
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)

    df.to_sql(table_name.lower(), con=engine, if_exists='replace', index=False)
