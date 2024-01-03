import os
import tkinter as tk
from tkinter import messagebox, ttk

# Function to edit and compile the Python file
def compile_file():
    # Get the user input from the GUI
    bot_id_input = bot_id_entry.get()
    chat_id_input = chat_id_entry.get()
    db_token_input = db_token_entry.get()

    # Open the Python file for editing
    with open("main.py", "r") as file:
        code = file.read()

    # Edit the code with the user input
    edited_code = code.replace('bot_id = "YOUR_BOT_TOKEN"', f'bot_id = "{bot_id_input}"')
    edited_code = edited_code.replace('chat_id = "YOUR_CHAT_ID"', f'chat_id = "{chat_id_input}"')
    edited_code = edited_code.replace('db_token = "YOUR_DROPBOX_TOKEN"', f'db_token = "{db_token_input}"')

    # Write the edited code back to the Python file
    with open("main.py", "w") as file:
        file.write(edited_code)

    # Compile the Python file using PyInstaller
    os.system("pyinstaller --onefile main.py")

    # Display success message
    messagebox.showinfo("Compilation Complete", "Executable file created!")

# Create the GUI
root = tk.Tk()
root.title("Python File Editor")
root.geometry("400x300")
root.configure(bg="#000000")

# Style for labels and buttons
style = ttk.Style()
style.configure("TLabel", foreground="#00FF00", background="#000000", font=("Courier", 12, "bold"))
style.configure("TButton", foreground="#00FF00", background="#000000", font=("Courier", 12, "bold"))

# Label and Entry for bot_id
bot_id_label = ttk.Label(root, text="Enter bot_id:")
bot_id_label.pack(pady=10)
bot_id_entry = ttk.Entry(root)
bot_id_entry.pack(pady=5)

# Label and Entry for chat_id
chat_id_label = ttk.Label(root, text="Enter chat_id:")
chat_id_label.pack(pady=10)
chat_id_entry = ttk.Entry(root)
chat_id_entry.pack(pady=5)

# Label and Entry for db_token
db_token_label = ttk.Label(root, text="Enter db_token:")
db_token_label.pack(pady=10)
db_token_entry = ttk.Entry(root)
db_token_entry.pack(pady=5)

# Button to trigger the file editing and compilation
button = ttk.Button(root, text="Compile", command=compile_file)
button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
