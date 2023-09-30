import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import psutil

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
            result_label.config(text=f"Changes applied {CHECKMARK_SYMBOL}")
            restart_option = messagebox.askyesno("Restart Deluge", "Please restart your Deluge client to apply changes.\nDo you want to restart Deluge desktop?")
            if restart_option:
                close_and_restart_deluge(deluge_install_folder)
        else:
            result_label.config(text="Changes not applied")
    else:
        gtk_3_0_folder = os.path.join(deluge_install_folder, SHARE_FOLDER, GTK_3_0_FOLDER)
        if not os.path.exists(gtk_3_0_folder):
            os.makedirs(gtk_3_0_folder)

        with open(settings_ini_path, 'w') as settings_ini_file:
            settings_ini_file.write("[Settings]\n")
            settings_ini_file.write(f"gtk-application-prefer-dark-theme={str(dark_theme).lower()}\n")
        result_label.config(text=f"Changes applied {CHECKMARK_SYMBOL}")
        restart_option = messagebox.askyesno("Restart Deluge", "Please restart your Deluge client to apply changes.\nDo you want to restart Deluge desktop?")
        if restart_option:
            close_and_restart_deluge(deluge_install_folder)

def close_and_restart_deluge(deluge_folder):
    deluge_exe_path = os.path.join(deluge_folder, "deluge.exe")
    if os.path.exists(deluge_exe_path):
        # Attempt to close Deluge gracefully
        try:
            deluge_process = get_deluge_process()
            if deluge_process:
                deluge_process.terminate()
                deluge_process.wait()
            subprocess.Popen([deluge_exe_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart Deluge desktop: {str(e)}")
    else:
        messagebox.showerror("Error", "Deluge desktop (deluge.exe) not found in the selected folder.")

def get_deluge_process():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = process.info['name']
            if process_name == 'deluge.exe':
                return psutil.Process(process.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def quit_application():
    window.quit()

# Create the main window
window = tk.Tk()
window.title(WINDOW_TITLE)

# Label and entry for folder selection
folder_label = tk.Label(window, text=FOLDER_LABEL_TEXT)
folder_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

entry_var = tk.StringVar()
folder_entry = tk.Entry(window, textvariable=entry_var, width=40)  # Increase width here
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

# Start the GUI main loop
window.mainloop()
