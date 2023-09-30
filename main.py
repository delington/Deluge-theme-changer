import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Constants
WINDOW_TITLE = "Deluge Theme Installer"
FOLDER_LABEL_TEXT = "Select Deluge Installation Folder:"
BROWSE_BUTTON_TEXT = "Browse"
APPLY_DARK_BUTTON_TEXT = "Apply Dark Theme"
APPLY_LIGHT_BUTTON_TEXT = "Apply Light Theme"
QUIT_BUTTON_TEXT = "Quit"
RESULT_LABEL_INITIAL_TEXT = ""
SHARE_FOLDER = "share"
GTK_3_0_FOLDER = "gtk-3.0"
SETTINGS_INI_FILE = "settings.ini"
CHECKMARK_SYMBOL = "✔️"  # Unicode checkmark symbol

def select_install_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_var.set(folder_selected)

def apply_dark_theme():
    apply_theme(True)

def apply_light_theme():
    apply_theme(False)

def apply_theme(dark_theme):
    deluge_install_folder = entry_var.get()
    settings_ini_path = os.path.join(deluge_install_folder, SHARE_FOLDER, GTK_3_0_FOLDER, SETTINGS_INI_FILE)

    if os.path.exists(settings_ini_path):
        response = messagebox.askquestion("File Exists", "The settings.ini file already exists. Do you want to override it?")
        if response == "yes":
            with open(settings_ini_path, 'w') as settings_ini_file:
                settings_ini_file.write("[Settings]\n")
                settings_ini_file.write(f"gtk-application-prefer-dark-theme={str(dark_theme).lower()}\n")
            result_label.config(text="Changes applied")
    else:
        gtk_3_0_folder = os.path.join(deluge_install_folder, SHARE_FOLDER, GTK_3_0_FOLDER)
        if not os.path.exists(gtk_3_0_folder):
            os.makedirs(gtk_3_0_folder)

        with open(settings_ini_path, 'w') as settings_ini_file:
            settings_ini_file.write("[Settings]\n")
            settings_ini_file.write(f"gtk-application-prefer-dark-theme={str(dark_theme).lower()}\n")
        result_label.config(text=f"Changes applied ${CHECKMARK_SYMBOL}")

def quit_application():
    window.quit()

# Create the main window
window = tk.Tk()
window.title(WINDOW_TITLE)

# Label and entry for folder selection
folder_label = tk.Label(window, text=FOLDER_LABEL_TEXT)
folder_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

entry_var = tk.StringVar()
folder_entry = tk.Entry(window, textvariable=entry_var)
folder_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

browse_button = tk.Button(window, text=BROWSE_BUTTON_TEXT, command=select_install_folder)
browse_button.grid(row=1, column=2, padx=20, pady=10)

# Apply dark theme button
apply_dark_button = tk.Button(window, text=APPLY_DARK_BUTTON_TEXT, command=apply_dark_theme)
apply_dark_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# Apply light theme button
apply_light_button = tk.Button(window, text=APPLY_LIGHT_BUTTON_TEXT, command=apply_light_theme)
apply_light_button.grid(row=2, column=2, padx=20, pady=10)

# Quit button
quit_button = tk.Button(window, text=QUIT_BUTTON_TEXT, command=quit_application)
quit_button.grid(row=3, column=1, padx=20, pady=10)

# Result label
result_label = tk.Label(window, text=RESULT_LABEL_INITIAL_TEXT)
result_label.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

# Checkmark label
checkmark_label = tk.Label(window)
checkmark_label.grid(row=5, column=2, padx=20, pady=10)

# Start the GUI main loop
window.mainloop()
