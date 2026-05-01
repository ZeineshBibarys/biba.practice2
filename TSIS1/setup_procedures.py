# setup_procedures.py
import psycopg2
from config import load_config

def apply_procedures():
    try:
        with open('TSIS1/procedures.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        params = load_config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_script)
                print("Процедуралар мен функциялар сәтті енгізілді!")
                
    except Exception as error:
        print(f"Қате: {error}")

if __name__ == '__main__':
    apply_procedures()