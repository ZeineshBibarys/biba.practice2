# phonebook.py
import psycopg2
import csv
import json
import os
from datetime import datetime
from config import load_config

def get_db_connection():
    return psycopg2.connect(**load_config())

# --- 1. Мәліметтерді импорттау және экспорттау ---

def import_from_csv(filename):
    """CSV-ден импорттау (email, birthday, group, phone, type)"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                with open(filename, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Контактіні қосу немесе жаңарту
                        cur.execute("CALL upsert_contact(%s, %s, %s)", 
                                    (row['name'], row.get('email'), row.get('birthday') or None))
                        # Телефонды қосу
                        cur.execute("CALL add_phone(%s, %s, %s)", 
                                    (row['name'], row['phone'], row.get('type', 'mobile')))
                        # Топқа қосу
                        if row.get('group'):
                            cur.execute("CALL move_to_group(%s, %s)", (row['name'], row['group']))
                conn.commit()
        print("CSV импорты сәтті аяқталды!")
    except Exception as e:
        print(f"CSV қатесі: {e}")

def export_to_json(filename):
    """Барлық мәліметті JSON-ға экспорттау"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.name, c.email, c.birthday, g.name as group_name,
                           json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON c.id = p.contact_id
                    GROUP BY c.id, g.name
                """)
                rows = cur.fetchall()
                data = []
                for r in rows:
                    data.append({
                        "name": r[0], "email": r[1], 
                        "birthday": str(r[2]) if r[2] else None,
                        "group": r[3], "phones": r[4]
                    })
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Мәліметтер {filename} файлына сақталды!")
    except Exception as e:
        print(f"Экспорт қатесі: {e}")

# --- 2. Іздеу және Пагинация ---

def search_contacts_ui():
    query = input("Іздеу үшін сөзді енгізіңіз (аты, email немесе телефон): ")
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            results = cur.fetchall()
            if not results:
                print("Ештеңе табылмады.")
                return
            for r in results:
                print(f"Аты: {r[0]} | Email: {r[1]} | Телефондар: {r[2]} | Топ: {r[3]}")
5
    # phonebook.py ішіндегі функцияны жаңарту
def view_paginated():
    limit = 5
    offset = 0
    while True:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_paginated_contacts(%s, %s)", (limit, offset))
                rows = cur.fetchall()
                
                # Егер мәлімет жоқ болса және бұл бірінші бет емес болса
                if not rows and offset > 0:
                    print("Бұл соңғы бет.")
                    offset -= limit
                    continue
                
                print(f"\n--- Бет: {(offset//limit)+1} ---")
                
                if not rows:
                    print("Базада ешқандай контакт жоқ.")
                else:
                    for r in rows:
                        # Бағандардың барын қауіпсіз тексеру
                        name = r[0] if len(r) > 0 else "белгісіз"
                        email = r[1] if len(r) > 1 else "белгісіз"
                        phones = r[2] if len(r) > 2 and r[2] else "жоқ"
                        group = r[3] if len(r) > 3 and r[3] else "жоқ"
                        
                        print(f"Аты: {name:<10} | Email: {email:<20} | Телефон: {phones:<20} | Топ: {group}")
                
                # ОСЫ БӨЛІК МІНДЕТТІ ТҮРДЕ БОЛУЫ КЕРЕК (Циклді тоқтату үшін)
                cmd = input("\n[n] Келесі, [p] Алдыңғы, [q] Шығу: ").lower()
                if cmd == 'n': 
                    offset += limit
                elif cmd == 'p': 
                    offset = max(0, offset - limit)
                elif cmd == 'q': 
                    break

# --- 3. Негізгі Меню ---

def main_menu():
    while True:
        print("\n--- PhoneBook (TSIS 1) ---")
        print("1. Жаңа контакт қосу/жаңарту (Upsert)")
        print("2. Телефон қосу (барына)")
        print("3. Топқа жылжыту")
        print("4. Кеңейтілген іздеу")
        print("5. Тізімді көру (Пагинация)")
        print("6. CSV-ден импорттау")
        print("7. JSON-ға экспорттау")
        print("0. Шығу")
        
        choice = input("Таңдауыңыз: ")
        
        if choice == '1':
            name = input("Аты: ")
            email = input("Email: ")
            bday = input("Туған күні (YYYY-MM-DD) немесе бос қалдырыңыз: ")
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL upsert_contact(%s, %s, %s)", (name, email, bday or None))
            print("Орындалды.")
        
        elif choice == '2':
            name = input("Контакт аты: ")
            phone = input("Телефон: ")
            ptype = input("Түрі (home, work, mobile): ")
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
                print("Телефон қосылды.")
            except Exception as e: print(e)

        elif choice == '4': search_contacts_ui()
        elif choice == '5': view_paginated()
        elif choice == '6':
            fname = input("CSV файл аты (мысалы, contacts.csv): ")
            if os.path.exists(fname): import_from_csv(fname)
            else: print("Файл табылмады.")
        elif choice == '7': export_to_json("contacts_backup.json")
        elif choice == '0': break
        else: print("Қате таңдау.")

if __name__ == '__main__':
    main_menu()