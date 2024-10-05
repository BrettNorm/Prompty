import tkinter as tk
from tkinter import filedialog

def on_click():
    folder_path = filedialog.askdirectory()
    if folder_path:
        print(f"Selected Folder: {folder_path}")  # For now, just print the selected folder

# Create the main application window
root = tk.Tk()
root.title("Select a Folder")

# Create a button that lets you select a folder
select_button = tk.Button(root, text="Select Folder", command=on_click)
select_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
