import tkinter as tk  # For the app window and widgets
import random         # To make random passwords
import string         # For letters, numbers, and symbols

# Basic settings
WHITE = "#ffffff"  # White color
FONT = ("Arial", 14)  # Normal text
HEADER_FONT = ("Arial", 20, "bold")  # Big bold text
TITLE_FONT = ("Arial", 24, "bold")   # Title text
PASSWORD_FILE = "passwords.txt"  # File where passwords are saved


# Make a random strong password
def generate_password(length=16):
    if length < 12:
        raise ValueError("Password must be at least 12 characters.")
    
    # Add one of each type of character
    chars = (
        random.choice(string.ascii_lowercase) +
        random.choice(string.ascii_uppercase) +
        random.choice(string.digits) +
        random.choice(string.punctuation) +
        ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length-4))
    )

    # Shuffle the password
    shuffled = list(chars)
    random.shuffle(shuffled)
    return ''.join(shuffled)


# Make a color between two colors
def shade_color(c1, c2, t):
    r1, g1, b1 = [int(c1[i:i+2], 16) for i in (1, 3, 5)]
    r2, g2, b2 = [int(c2[i:i+2], 16) for i in (1, 3, 5)]
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


# Make a gradient image
def make_gradient_image(width, height, c1="#800080", c2="#DDA0DD"):
    img = tk.PhotoImage(width=width, height=height)
    for y in range(height):
        color = shade_color(c1, c2, y / height)
        img.put(color, to=(0, y, width, y + 1))
    return img


# Add gradient background to a frame
def apply_gradient_bg(frame, width=360, height=640):
    img = make_gradient_image(width, height)
    bg_label = tk.Label(frame, image=img)
    bg_label.image = img  # Keep image from being deleted
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()
    return bg_label


# Save password to file
def save_password(pw):
    with open(PASSWORD_FILE, "a") as f:
        f.write(pw + "\n")


# Load saved passwords into the list
def load_passwords():
    try:
        with open(PASSWORD_FILE) as f:
            for line in f:
                password_listbox.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass


# Delete password from file
def delete_password_from_file(pw):
    with open(PASSWORD_FILE, "r") as f:
        lines = f.readlines()
    with open(PASSWORD_FILE, "w") as f:
        for line in lines:
            if line.strip() != pw:
                f.write(line)


# Delete selected password
def delete_password():
    selected = password_listbox.get(tk.ACTIVE)
    if selected:
        password_listbox.delete(tk.ACTIVE)
        delete_password_from_file(selected)


# Show a frame (screen)
def show_frame(frame):
    frame.tkraise()


# Make the main window
root = tk.Tk()
root.title("KeyPassHub")  # App name
root.geometry("360x640")  # App size
root.resizable(False, False)  # Can't resize

# Hold all pages in one container
container = tk.Frame(root)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create each screen (main, generator, bank)
frames = {}
for name in ("main", "generator", "bank"):
    frm = tk.Frame(container)
    frm.grid(row=0, column=0, sticky="nsew")
    apply_gradient_bg(frm)
    frames[name] = frm

# Main menu screen
main = frames["main"]
tk.Label(main, text="KeyPassHub", fg="black", bg=WHITE, font=TITLE_FONT).pack(pady=30)

# Makes a white round button
def styled_button(parent, text, command):
    frame = tk.Frame(parent, bg="white", bd=0)
    canvas = tk.Canvas(frame, width=240, height=50, bg="white", highlightthickness=0)
    canvas.pack()
    radius = 20
    canvas.create_oval(0, 0, 2 * radius, 2 * radius, fill="white", outline="white")
    canvas.create_oval(240 - 2 * radius, 0, 240, 2 * radius, fill="white", outline="white")
    canvas.create_rectangle(radius, 0, 240 - radius, 2 * radius, fill="white", outline="white")
    button = tk.Button(frame, text=text, command=command, font=FONT,
                       fg="black", bg="white", relief="flat", bd=0, highlightthickness=0)
    button.place(relx=0.5, rely=0.5, anchor="center", width=240, height=40)
    return frame

# Add buttons to main menu
styled_button(main, " Password Generation", lambda: show_frame(frames["generator"])).pack(pady=15)
styled_button(main, " Password Bank", lambda: show_frame(frames["bank"])).pack(pady=15)
styled_button(main, "❌ Exit App", root.destroy).pack(pady=25)

# Password generator screen
generator = frames["generator"]
password = tk.StringVar()  # Stores the generated password

tk.Label(generator, text="Password Generator", fg="black", bg=WHITE, font=HEADER_FONT).pack(pady=20)
tk.Label(generator, textvariable=password, font=FONT, bg=WHITE, fg="black", wraplength=320).pack(pady=20, ipadx=10, ipady=10)

# Button to make new password
def generate():
    try:
        password.set(generate_password())
    except Exception as e:
        password.set(str(e))

# Add current password to the list
def add_to_bank():
    pw = password.get()
    if pw:
        save_password(pw)
        password_listbox.insert(tk.END, pw)

# Buttons on generator screen
styled_button(generator, " Generate", generate).pack(pady=10)
styled_button(generator, "➕ Add to Password Bank", add_to_bank).pack(pady=10)
styled_button(generator, "⬅ Back", lambda: show_frame(frames["main"])).pack(pady=30)

# Password bank screen
bank = frames["bank"]
tk.Label(bank, text="Password Bank", fg="black", bg=WHITE, font=HEADER_FONT).pack(pady=20)

# Text box to type new password
password_entry = tk.Entry(bank, font=FONT, bg=WHITE, fg="black")
password_entry.pack(pady=10, ipadx=10, ipady=5)

# Add typed password to list
def add_password():
    pw = password_entry.get()
    if pw:
        save_password(pw)
        password_listbox.insert(tk.END, pw)
        password_entry.delete(0, "end")

styled_button(bank, "➕ Add Password", add_password).pack(pady=10)

# Show saved passwords with scroll
listbox_frame = tk.Frame(bank, bg=WHITE)
listbox_frame.pack(pady=10, padx=10)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# List where passwords appear
password_listbox = tk.Listbox(listbox_frame, font=FONT, bg=WHITE, fg="black",
                              height=8, width=28, yscrollcommand=scrollbar.set,
                              relief="solid", borderwidth=1)
password_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=password_listbox.yview)

# Right-click menu to delete password
def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Delete", command=delete_password)

password_listbox.bind("<Button-3>", show_context_menu)

# Back to main menu button
styled_button(bank, "⬅ Back", lambda: show_frame(frames["main"])).pack(pady=30)

# Start app: load saved passwords and show main screen
load_passwords()
show_frame(frames["main"])
root.mainloop()
