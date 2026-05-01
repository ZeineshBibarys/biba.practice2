import psycopg2
from config import load_config

def connect():
    conn = None
    try:
        # config.py-дан мәліметтерді оқу
        params = load_config()
        print("PostgreSQL базасына қосылуда...")
        
        # Базаға қосылу
        conn = psycopg2.connect(**params)
        
        # Курсор құру
        crsr = conn.cursor()
        
        print("Қосылым сәтті өтті!")
        
        # Базаның версиясын тексеру
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(f"PostgreSQL нұсқасы: {db_version[0]}")
        
        # Курсорды жабу
        crsr.close()
        return conn
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Қате шықты: {error}")
        return None

if __name__ == '__main__':
    # Файлды жүргізген кезде қосылымды тексеру
    test_conn = connect()
    if test_conn:
        test_conn.close()