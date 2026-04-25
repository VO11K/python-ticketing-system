import sqlite3
from datetime import datetime

DB_NAME = "tickets.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_ticket():
    title = input("Ticket title: ")
    description = input("Description: ")
    category = input("Category (Hardware/Software/Network/Other): ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (title, description, category, created_at)
        VALUES (?, ?, ?, ?)
    """, (title, description, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

    print("Ticket created successfully.")


def view_tickets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    conn.close()

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(f"""
ID: {ticket[0]}
Title: {ticket[1]}
Description: {ticket[2]}
Category: {ticket[3]}
Status: {ticket[4]}
Created At: {ticket[5]}
-------------------------
""")


def update_ticket_status():
    ticket_id = input("Enter ticket ID: ")
    new_status = input("New status (Open/In Progress/Closed): ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE id = ?
    """, (new_status, ticket_id))

    conn.commit()
    conn.close()

    print("Ticket status updated.")


def delete_ticket():
    ticket_id = input("Enter ticket ID to delete: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))

    conn.commit()
    conn.close()

    print("Ticket deleted.")


def main_menu():
    while True:
        print("""
=== Ticketing System ===
1. Create Ticket
2. View Tickets
3. Update Ticket Status
4. Delete Ticket
5. Exit
""")

        choice = input("Choose an option: ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            update_ticket_status()
        elif choice == "4":
            delete_ticket()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


create_tables()
main_menu()