from src.utils.database_connection import get_db_engine

engine = get_db_engine()

with engine.connect() as conn:
    print("✅ Connected successfully!")
