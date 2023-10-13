'''
Assignment 3
Course: IoT
Name: Yi Siang Chang
Date: 2023-09-13
'''

### Import required libraries

import tkinter as tk
# tkinter is a standard GUI library in Python.

from tkinter import ttk, messagebox
# ttk provides access to the themed widgets.

import random
import string
# random and string are modules to help with password generation.

def generateStrongPassword(length):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    if length < 6:
        return "Password length must be more than 5!"

    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    for i in range(length - 4):
        password.append(random.choice(all_characters))
    random.shuffle(password)
    return ''.join(password)

def generateAndDisplay():
# function gets the desired password length and the number of passwords
# the user wants to generate from the GUI input fields.

# When the "Generate" button is clicked, the generateAndDisplay function
# is called to process the user's input, generate passwords, and display them.

    try:
        num_passwords = int(num_pass_var.get())
        password_length = int(pass_length_var.get())
        if password_length < 6:
            messagebox.showerror("Error", "Password length must be more than 5!")
            return
        generated_passwords.delete(1.0, tk.END)
        for _ in range(num_passwords):
            password = generateStrongPassword(password_length)
            generated_passwords.insert(tk.END, password + "\n")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for the fields!")

### GUI Setup

app = tk.Tk()  # Creates the main application window.
app.title("Password Generator")

# ttk.Frame, ttk.Label, ttk.Entry, ttk.Button, and tk.Text
# are all various widgets (GUI components) used to build the interface.
# Each of them has various configurations

main_frame = ttk.Frame(app, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
# .grid() method is used for organizing and positioning the widgets.
# The parameters like column, row, pady, and padx determine the position
# and spacing of the widgets.

num_pass_label = ttk.Label(main_frame, text="Number of Passwords:")
num_pass_label.grid(column=0, row=0, sticky=tk.W, pady=5, padx=5)

num_pass_var = tk.StringVar()
# num_pass_var is used to retrieve or set the content of the ttk.Entry widgets.
num_pass_entry = ttk.Entry(main_frame, textvariable=num_pass_var, width=5)
num_pass_entry.grid(column=1, row=0, pady=5, padx=5)

pass_length_label = ttk.Label(main_frame, text="Password Length:")
pass_length_label.grid(column=0, row=1, sticky=tk.W, pady=5, padx=5)

pass_length_var = tk.StringVar()
# pass_length_var is used to retrieve or set the content of the ttk.Entry widgets.
pass_length_entry = ttk.Entry(main_frame, textvariable=pass_length_var, width=5)
pass_length_entry.grid(column=1, row=1, pady=5, padx=5)

generate_button = ttk.Button(main_frame, text="Generate", command=generateAndDisplay)
generate_button.grid(column=0, row=2, columnspan=2, pady=20)

generated_passwords_label = ttk.Label(main_frame, text="Generated Passwords:")
generated_passwords_label.grid(column=0, row=3, columnspan=2, sticky=tk.W, pady=5)

generated_passwords = tk.Text(main_frame, wrap=tk.WORD, width=40, height=10)
generated_passwords.grid(column=0, row=4, columnspan=2, pady=5)

app.mainloop()
# This line is at the end, and it starts the main event loop of the GUI application,
# waiting for user interactions.