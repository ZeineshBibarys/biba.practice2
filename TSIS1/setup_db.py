import psycopg2
from config import load_config

def create_tables():
    commands = []
    try:
        # SQL файлды оқу
        with open('TSIS1/schema.sql', 'r') as f:
            # SQL командаларын бөліп алу
            sql_script = f.read()
        
        params = load_config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Скриптті орындау
                cur.execute(sql_script)
                print("Кестелер сәтті құрылды!")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Қате: {error}")

if __name__ == '__main__':
    create_tables()