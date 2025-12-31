# Contact Management System
# Week 3 Project - Functions & Dictionaries

import json
import re
from datetime import datetime
import csv
import os

FILENAME = "contacts_data.json"

# ---------------- DISPLAY HELPERS ----------------

def print_header():
    print("=" * 50)
    print("      CONTACT MANAGEMENT SYSTEM")
    print("=" * 50)
    print()

def print_menu():
    print("=" * 30)
    print("          MAIN MENU")
    print("=" * 30)
    print("1. Add New Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. View All Contacts")
    print("6. Export to CSV")
    print("7. View Statistics")
    print("8. Exit")
    print("=" * 30)

# ---------------- VALIDATION ----------------

def validate_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ---------------- FILE HANDLING ----------------

def load_contacts():
    if not os.path.exists(FILENAME):
        print("✅ No existing contacts file found. Starting fresh.\n")
        return {}
    with open(FILENAME, "r") as file:
        return json.load(file)

def save_contacts(contacts):
    with open(FILENAME, "w") as file:
        json.dump(contacts, file, indent=4)
    print(f"✅ Contacts saved to {FILENAME}")

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
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if not email or validate_email(email):
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    contacts[name] = {
        "phone": cleaned_phone,
        "email": email if email else None,
        "address": address if address else None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    print(f"✅ Contact '{name}' added successfully!")
    save_contacts(contacts)
    return contacts

def search_contacts(contacts):
    term = input("Enter name to search: ").lower()
    results = []

    for name, info in contacts.items():
        if term in name.lower():
            results.append((name, info))

    if not results:
        print("No contacts found.")
        return

    print(f"\nFound {len(results)} contact(s):")
    print("-" * 50)

    for i, (name, info) in enumerate(results, 1):
        print(f"{i}. {name}")
        print(f"   📞 Phone: {info['phone']}")
        if info["email"]:
            print(f"   📧 Email: {info['email']}")
        if info["address"]:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}\n")

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
    print(f"✅ Contact '{name}' updated successfully!")
    save_contacts(contacts)
    return contacts

def delete_contact(contacts):
    name = input("Enter contact name to delete: ").strip()

    if name not in contacts:
        print("Contact not found!")
        return contacts

    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        print("✅ Contact deleted!")
        save_contacts(contacts)
    return contacts

def display_all_contacts(contacts):
    if not contacts:
        print("No contacts available.")
        return

    print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
    print("=" * 60)

    for name, info in contacts.items():
        print(f"👤 {name}")
        print(f"   📞 {info['phone']}")
        if info["email"]:
            print(f"   📧 {info['email']}")
        print(f"   👥 {info['group']}")
        print("-" * 40)

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

    print("✅ Contacts exported to contacts.csv")

def statistics(contacts):
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {len(contacts)}\n")

    groups = {}
    for info in contacts.values():
        groups[info["group"]] = groups.get(info["group"], 0) + 1

    print("Contacts by Group:")
    for group, count in groups.items():
        print(f"  {group}: {count} contact(s)")

# ---------------- MENU ----------------

def main_menu():
    print_header()
    contacts = load_contacts()

    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ")

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
        elif choice == "8":
            save_contacts(contacts)
            print("\n" + "=" * 50)
            print("Thank you for using Contact Management System!")
            print("=" * 50)
            break
        else:
            print("Invalid choice!")

# ---------------- MAIN ----------------

if __name__ == "__main__":
    main_menu()
