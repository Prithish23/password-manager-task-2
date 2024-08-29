
import os
import json
import random
import string
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog, font

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()


def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message


def save_password(website, username, password, category, key):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
    else:
        data = {}

    encrypted_password = encrypt_message(password, key)
    
    if category not in data:
        data[category] = []
    
    data[category].append({
        "website": website,
        "username": username,
        "password": encrypted_password.decode()
    })
    
    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)
    
    messagebox.showinfo("Success", "Password saved successfully!")

def retrieve_password(category, key):
    if not os.path.exists("passwords.json"):
        messagebox.showwarning("Warning", "No passwords stored yet.")
        return

    with open("passwords.json", "r") as file:
        data = json.load(file)
    
    if category in data:
        passwords = ""
        for entry in data[category]:
            decrypted_password = decrypt_message(entry["password"].encode(), key)
            passwords += f"Website: {entry['website']}, Username: {entry['username']}, Password: {decrypted_password}\n"
        messagebox.showinfo(f"Passwords in {category}", passwords)
    else:
        messagebox.showwarning("Warning", "Category not found.")


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.key = self.load_or_generate_key()

        # Set custom fonts
        self.custom_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Save Password
        tk.Label(root, text="Website:", font=self.custom_font, bg="#e6f7ff").grid(row=0, column=0, padx=10, pady=10)
        self.website_entry = tk.Entry(root, font=self.custom_font)
        self.website_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Username:", font=self.custom_font, bg="#e6f7ff").grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(root, font=self.custom_font)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Password:", font=self.custom_font, bg="#e6f7ff").grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(root, font=self.custom_font)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(root, text="Category:", font=self.custom_font, bg="#e6f7ff").grid(row=3, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(root, font=self.custom_font)
        self.category_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(root, text="Save Password", command=self.save_password_gui, font=self.button_font, bg="#b3e6ff").grid(row=4, column=0, columnspan=2, pady=10)

        # Retrieve Password
        tk.Button(root, text="Retrieve Passwords by Category", command=self.retrieve_password_gui, font=self.button_font, bg="#b3e6ff").grid(row=5, column=0, columnspan=2, pady=10)

        # Generate Strong Password
        tk.Button(root, text="Generate Strong Password", command=self.generate_password_gui, font=self.button_font, bg="#b3e6ff").grid(row=6, column=0, columnspan=2, pady=10)

        # Set background color for the root window
        root.configure(bg="#e6f7ff")

    def load_or_generate_key(self):
        if not os.path.exists("key.key"):
            generate_key()
        return load_key()

    def save_password_gui(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        category = self.category_entry.get()

        if website and username and password and category:
            save_password(website, username, password, category, self.key)
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def retrieve_password_gui(self):
        category = simpledialog.askstring("Input", "Enter the category:", parent=self.root)
        if category:
            retrieve_password(category, self.key)

    def generate_password_gui(self):
        length = simpledialog.askinteger("Input", "Enter the password length:", minvalue=8, maxvalue=32, parent=self.root)
        if length:
            password = generate_password(length)
            messagebox.showinfo("Generated Password", f"Your generated password is: {password}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
 
