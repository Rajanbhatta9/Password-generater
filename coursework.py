import json
import os
import getpass

PASSWORD_DATA_FILE = "passwords.json"
MASTER_PASSWORD_STORAGE_FILE = "master_password.txt"

def load_password_data():
    if os.path.exists(PASSWORD_DATA_FILE):
        with open(PASSWORD_DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

def save_password_data(passwords):
    with open(PASSWORD_DATA_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

def store_password(passwords, website, username, password):
    passwords[website] = {'username': username, 'password': password}
    save_password_data(passwords)
    print("Password added successfully.")

def retrieve_password(passwords, website):
    if website in passwords:
        return passwords[website]
    else:
        print("Password not found.")

def delete_password(passwords, website):
    if website in passwords:
        del passwords[website]
        save_password_data(passwords)
        print("Password removed successfully.")
    else:
        print("Password not found.")

def view_passwords(passwords):
    for website, info in passwords.items():
        print(f"Website: {website}")
        print(f"Username: {info['username']}")
        print(f"Password: {info['password']}")
        print()

def initialize_master_password():
    master_password = getpass.getpass("Set Master Password: ")
    with open(MASTER_PASSWORD_STORAGE_FILE, "w") as file:
        file.write(master_password)

def verify_master_password():
    if not os.path.exists(MASTER_PASSWORD_STORAGE_FILE):
        initialize_master_password()
    else:
        with open(MASTER_PASSWORD_STORAGE_FILE, "r") as file:
            master_password = file.readline().strip()
        attempt = getpass.getpass("Enter Master Password: ")
        if attempt != master_password:
            print("Incorrect Master Password.")
            return False
    return True

def main():
    if not verify_master_password():
        return

    passwords = load_password_data()

    while True:
        print("\nPassword Manager Menu:")
        print("1. Add a password")
        print("2. Retrieve a password")
        print("3. Remove a password")
        print("4. View stored passwords")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            store_password(passwords, website, username, password)
        elif choice == "2":
            website = input("Enter website: ")
            password_info = retrieve_password(passwords, website)
            if password_info:
                print(f"Website: {website}")
                print(f"Username: {password_info['username']}")
                print(f"Password: {password_info['password']}")
        elif choice == "3":
            website = input("Enter website to remove: ")
            delete_password(passwords, website)
        elif choice == "4":
            view_passwords(passwords)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
