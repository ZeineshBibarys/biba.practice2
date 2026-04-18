import csv
import psycopg2
from connect import get_connection

def setup_database(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()
    print("Table 'contacts' is ready.")

def import_csv(conn, filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            insert_query = "INSERT INTO contacts (username, phone) VALUES (%s, %s)"
            with conn.cursor() as cur:
                for row in reader:
                    cur.execute(insert_query, (row[0], row[1]))
            conn.commit()
            print(f"Successfully imported data from {filename}.")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def add_contact(conn):
    username = input("Enter username: ")
    phone = input("Enter phone number: ")
    insert_query = "INSERT INTO contacts (username, phone) VALUES (%s, %s)"
    with conn.cursor() as cur:
        cur.execute(insert_query, (username, phone))
        conn.commit()
    print(f"Contact '{username}' added successfully.")

def update_contact(conn):
    target_username = input("Enter the username of the contact to update: ")
    print("1. Update Username\n2. Update Phone Number")
    choice = input("What would you like to update? (1/2): ")
    
    with conn.cursor() as cur:
        if choice == '1':
            new_name = input("Enter new username: ")
            cur.execute("UPDATE contacts SET username = %s WHERE username = %s", (new_name, target_username))
        elif choice == '2':
            new_phone = input("Enter new phone number: ")
            cur.execute("UPDATE contacts SET phone = %s WHERE username = %s", (new_phone, target_username))
        else:
            print("Invalid choice.")
            return
            
        if cur.rowcount > 0:
            print("Contact updated successfully.")
            conn.commit()
        else:
            print("Contact not found.")

def query_contacts(conn):
    print("1. Search by exact username\n2. Search by phone prefix")
    choice = input("Choose a filter (1/2): ")
    
    with conn.cursor() as cur:
        if choice == '1':
            name = input("Enter username: ")
            cur.execute("SELECT id, username, phone FROM contacts WHERE username = %s", (name,))
        elif choice == '2':
            prefix = input("Enter phone prefix (e.g., 555): ")
            cur.execute("SELECT id, username, phone FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))
        else:
            print("Invalid choice.")
            return

        results = cur.fetchall()
        if results:
            print("\n--- Search Results ---")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
            print("----------------------")
        else:
            print("No contacts found.")

def delete_contact(conn):
    print("1. Delete by username\n2. Delete by phone")
    choice = input("Choose deletion method (1/2): ")
    
    with conn.cursor() as cur:
        if choice == '1':
            name = input("Enter username to delete: ")
            cur.execute("DELETE FROM contacts WHERE username = %s", (name,))
        elif choice == '2':
            phone = input("Enter phone number to delete: ")
            cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
        else:
            print("Invalid choice.")
            return

        if cur.rowcount > 0:
            print("Contact deleted successfully.")
            conn.commit()
        else:
            print("Contact not found.")

def main():
    conn = get_connection()
    if not conn:
        return

    setup_database(conn)

    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Import contacts from CSV")
        print("2. Add new contact manually")
        print("3. Update existing contact")
        print("4. Search contacts")
        print("5. Delete a contact")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            import_csv(conn, 'contacts.csv')
        elif choice == '2':
            add_contact(conn)
        elif choice == '3':
            update_contact(conn)
        elif choice == '4':
            query_contacts(conn)
        elif choice == '5':
            delete_contact(conn)
        elif choice == '6':
            print("Closing PhoneBook...")
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()