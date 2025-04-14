from dotenv import load_dotenv
from src.utils.database_connection import get_db_engine

load_dotenv()


def save_to_postgres(df, table_name):
    """
    Save the stock data DataFrame to PostgreSQL.
    """
    engine = get_db_engine()

    df.to_sql(table_name.lower(), con=engine, if_exists='append', index=False)
