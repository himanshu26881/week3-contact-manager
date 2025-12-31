# Contact Management System
# Week 3 Project - Functions & Dictionaries

import json
import re
from datetime import datetime
import csv

FILENAME = "contacts_data.json"

# ---------------- VALIDATION ----------------

def validate_phone(phone):
    """Validate phone number format"""
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ---------------- FILE HANDLING ----------------

def load_contacts():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_contacts(contacts):
    with open(FILENAME, "w") as file:
        json.dump(contacts, file, indent=4)

# ---------------- CRUD OPERATIONS ----------------

def add_contact(contacts):
    print("\n--- ADD NEW CONTACT ---")

    while True:
        name = input("Enter contact name: ").strip()
        if name:
            if name in contacts:
                print("Contact already exists!")
                return contacts
            break
        print("Name cannot be empty!")

    while True:
        phone = input("Enter phone number: ").strip()
        valid, cleaned_phone = validate_phone(phone)
        if valid:
            break
        print("Invalid phone number!")

    while True:
        email = input("Enter email (optional): ").strip()
        if not email or validate_email(email):
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Family/Work): ").strip() or "Other"

    contacts[name] = {
        "phone": cleaned_phone,
        "email": email if email else None,
        "address": address if address else None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    save_contacts(contacts)
    print("✅ Contact added successfully!")
    return contacts

def search_contacts(contacts):
    term = input("Enter name to search: ").lower()
    found = False

    for name, info in contacts.items():
        if term in name.lower():
            print_contact(name, info)
            found = True

    if not found:
        print("No contacts found.")

def update_contact(contacts):
    name = input("Enter contact name to update: ").strip()

    if name not in contacts:
        print("Contact not found!")
        return contacts

    contact = contacts[name]

    phone = input("New phone (Enter to skip): ").strip()
    if phone:
        valid, cleaned_phone = validate_phone(phone)
        if valid:
            contact["phone"] = cleaned_phone

    email = input("New email (Enter to skip): ").strip()
    if email and validate_email(email):
        contact["email"] = email

    address = input("New address (Enter to skip): ").strip()
    if address:
        contact["address"] = address

    group = input("New group (Enter to skip): ").strip()
    if group:
        contact["group"] = group

    contact["updated_at"] = datetime.now().isoformat()
    save_contacts(contacts)
    print("✅ Contact updated successfully!")
    return contacts

def delete_contact(contacts):
    name = input("Enter contact name to delete: ").strip()

    if name not in contacts:
        print("Contact not found!")
        return contacts

    confirm = input("Are you sure? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        save_contacts(contacts)
        print("✅ Contact deleted!")
    return contacts

def display_all_contacts(contacts):
    if not contacts:
        print("No contacts available.")
        return

    for name, info in contacts.items():
        print_contact(name, info)

def print_contact(name, info):
    print("-" * 40)
    print(f"Name   : {name}")
    print(f"Phone  : {info['phone']}")
    if info["email"]:
        print(f"Email  : {info['email']}")
    if info["address"]:
        print(f"Address: {info['address']}")
    print(f"Group  : {info['group']}")

# ---------------- EXTRA FEATURES ----------------

def export_to_csv(contacts):
    with open("contacts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])

        for name, info in contacts.items():
            writer.writerow([
                name,
                info["phone"],
                info["email"],
                info["address"],
                info["group"]
            ])
    print("✅ Exported to contacts.csv")

def statistics(contacts):
    print(f"Total contacts: {len(contacts)}")

# ---------------- MENU ----------------

def main_menu():
    contacts = load_contacts()

    while True:
        print("\n📞 CONTACT MANAGEMENT SYSTEM")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display All")
        print("6. Export to CSV")
        print("7. Statistics")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            contacts = add_contact(contacts)
        elif choice == "2":
            search_contacts(contacts)
        elif choice == "3":
            contacts = update_contact(contacts)
        elif choice == "4":
            contacts = delete_contact(contacts)
        elif choice == "5":
            display_all_contacts(contacts)
        elif choice == "6":
            export_to_csv(contacts)
        elif choice == "7":
            statistics(contacts)
        elif choice == "0":
            save_contacts(contacts)
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

# ---------------- MAIN ----------------

if __name__ == "__main__":
    main_menu()
