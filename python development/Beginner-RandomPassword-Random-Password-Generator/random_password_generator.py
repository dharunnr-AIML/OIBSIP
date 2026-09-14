import random
import string
import tkinter as tk
from tkinter import messagebox


def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4.")
            return

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")


def copy_password():
    password = password_entry.get()

    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "Generate a password first.")


root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x350")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Random Password Generator",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=25)

tk.Label(
    root,
    text="Password Length",
    font=("Arial", 12)
).pack()

length_entry = tk.Entry(root, width=25)
length_entry.pack(pady=8)
length_entry.insert(0, "12")

generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    font=("Arial", 12, "bold")
)
generate_button.pack(pady=12)

tk.Label(
    root,
    text="Generated Password",
    font=("Arial", 12)
).pack()

password_entry = tk.Entry(root, width=40, font=("Arial", 12))
password_entry.pack(pady=8)

copy_button = tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    font=("Arial", 11, "bold")
)
copy_button.pack(pady=12)

root.mainloop()