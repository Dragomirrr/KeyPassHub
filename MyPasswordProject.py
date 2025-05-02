import tkinter as tk
import random
import string

# Colors and font
BLACK = "#000000"
WHITE = "#ffffff"
FONT = ("Arial", 14)
PASSWORD_FILE = "passwords.txt"  # File to save passwords

# Generate random password
def generate_password(length=16):
    if length < 12:
        raise ValueError("Password must be at least 12 characters long.")

    # Ensure password contains all character types
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    symbol = random.choice(string.punctuation)

    # Add random characters to the password
    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + string.punctuation
    remaining_chars = random.choices(all_chars, k=remaining_length)

    # Combine and shuffle
    password = list(lowercase + uppercase + digit + symbol + ''.join(remaining_chars))
    random.shuffle(password)

    return ''.join(password)

# Show password generator
def show_generator():
    win = tk.Toplevel(root)
    win.title("Password Generator")
    win.configure(bg=BLACK)

    # Set the window size to screen size, but keep the border
    win.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    def close_window():
        win.destroy()

    def generate():
        try:
            password.set(generate_password())
        except ValueError as e:
            password.set(str(e))

    def add_to_bank():
        new_password = password.get()
        if new_password:
            save_password(new_password)
            password_listbox.insert(tk.END, new_password)

    password = tk.StringVar()
    tk.Label(win, text="Password Generator", bg=BLACK, fg=WHITE, font=("Arial", 24)).pack(pady=20)

    output_label = tk.Label(win, textvariable=password, font=("Arial", 18), bg=WHITE, fg=BLACK, wraplength=1000)
    output_label.pack(pady=20, ipadx=30, ipady=15)

    tk.Button(win, text="Generate", command=generate, font=FONT, bg=WHITE, fg=BLACK, height=2).pack(pady=10, ipadx=20)
    
    # Button to add generated password to the list
    tk.Button(win, text="Add to Password Bank", command=add_to_bank, font=FONT, bg=WHITE, fg=BLACK, height=2).pack(pady=10, ipadx=20)
    
    tk.Button(win, text="Back", command=close_window, font=FONT, bg=BLACK, fg=WHITE, height=2).pack(pady=40)

# Show password bank
def show_bank():
    win = tk.Toplevel(root)
    win.title("Password Bank")
    win.configure(bg=BLACK)

    # Set the window size to screen size, but keep the border
    win.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    def close_window():
        win.destroy()

    def add_password():
        new_password = password_entry.get()
        if new_password:
            save_password(new_password)
            password_listbox.insert(tk.END, new_password)
            password_entry.delete(0, tk.END)  # Clear the entry after adding

    # Widgets for Password Bank
    tk.Label(win, text="Password Bank", bg=BLACK, fg=WHITE, font=("Arial", 24)).pack(pady=20)

    password_entry = tk.Entry(win, font=FONT, bg=WHITE, fg=BLACK)
    password_entry.pack(pady=10, ipadx=30, ipady=10)

    add_button = tk.Button(win, text="Add Password", command=add_password, font=FONT, bg=WHITE, fg=BLACK, height=2)
    add_button.pack(pady=10, ipadx=20)

    # Listbox to display passwords
    global password_listbox  # Make the listbox accessible in other functions
    password_listbox = tk.Listbox(win, font=FONT, bg=WHITE, fg=BLACK, height=10, width=50)
    password_listbox.pack(pady=20, padx=20)

    tk.Button(win, text="Back", command=close_window, font=FONT, bg=BLACK, fg=WHITE, height=2).pack(pady=40)

    # Load saved passwords
    load_passwords()

# Save a password to a file
def save_password(password):
    with open(PASSWORD_FILE, "a") as file:
        file.write(password + "\n")

# Load saved passwords into the list
def load_passwords():
    try:
        with open(PASSWORD_FILE, "r") as file:
            passwords = file.readlines()
            for password in passwords:
                password_listbox.insert(tk.END, password.strip())  # Remove extra space
    except FileNotFoundError:
        pass  # If no file, just continue

# Main window
root = tk.Tk()
root.title("KeyPassHub")  # App name changed to KeyPassHub
root.configure(bg=BLACK)

# Set the window size to screen size, but keep the border
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# Title
tk.Label(root, text="KeyPassHub", bg=BLACK, fg=WHITE, font=("Arial", 32)).pack(pady=40)

# Button to open password generator
tk.Button(root, text="Password Generation", command=show_generator, font=FONT, bg=WHITE, fg=BLACK, height=2).pack(pady=20, ipadx=20, ipady=10)

# Button to open password bank
tk.Button(root, text="Password Bank", command=show_bank, font=FONT, bg=WHITE, fg=BLACK, height=2).pack(pady=20, ipadx=20, ipady=10)

# Exit button
tk.Button(root, text="Exit App", command=root.destroy, font=FONT, bg=BLACK, fg=WHITE, height=2).pack(pady=20)

root.mainloop()