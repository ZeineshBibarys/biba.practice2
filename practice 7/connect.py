import psycopg2
from config import load_config

def get_connection():
    conn = None
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection error: {error}")
        return None