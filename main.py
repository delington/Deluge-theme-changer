import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.colorchooser import askcolor
import subprocess
import psutil

# Constants
WINDOW_TITLE = "Deluge Theme Installer"
FOLDER_LABEL_TEXT = "Select Deluge Installation Folder:"
BROWSE_BUTTON_TEXT = "Browse"
APPLY_DARK_BUTTON_TEXT = "Apply Dark Theme"
APPLY_LIGHT_BUTTON_TEXT = "Apply Light Theme"
APPLY_CUSTOM_THEME_BUTTON_TEXT = "Custom Theme"
QUIT_BUTTON_TEXT = "Quit"
RESULT_LABEL_INITIAL_TEXT = ""
FOLDER_SHARE = "share"
FOLDER_THEMES = "themes"
FOLDER_NASTER = "Naster"
FOLDER_GTK_3_0 = "gtk-3.0"
FILE_GTK_CSS = "gtk.css"
FILE_SETTINGS_INI = "settings.ini"

def select_install_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_var.set(folder_selected)

def get_GTK_folder_path():
    deluge_install_folder = entry_var.get()
    return os.path.join(deluge_install_folder, FOLDER_SHARE, FOLDER_GTK_3_0)

def get_settings_path():
    return os.path.join(get_GTK_folder_path(), FILE_SETTINGS_INI)

def get_themes_css_path():
    deluge_install_folder = entry_var.get()
    return os.path.join(deluge_install_folder, FOLDER_SHARE, FOLDER_THEMES, FOLDER_NASTER, FOLDER_GTK_3_0, FILE_GTK_CSS)

def apply_dark_theme():
    apply_theme(True)

def apply_light_theme():
    apply_theme(False)

def modify_theme_settings_file(settings_ini_path, apply_theme_text):
    with open(settings_ini_path, 'w') as settings_ini_file:
        settings_ini_file.write("[Settings]\n")
        settings_ini_file.write(apply_theme_text)

def ask_restart_option():
    restart_option = messagebox.askyesno("Restart Deluge", "Please restart your Deluge client to apply changes.\nDo you want to restart Deluge desktop?")
    if restart_option:
        deluge_install_folder = entry_var.get()
        close_and_restart_deluge(deluge_install_folder)

def apply_theme(is_dark_apply):
    settings_ini_path = get_settings_path()

    if os.path.exists(settings_ini_path):
        response = messagebox.askquestion("File Exists", "The settings.ini file already exists. Do you want to override it?")
        if response == "yes":
            apply_theme_text = f"gtk-application-prefer-dark-theme={str(is_dark_apply).lower()}\n"
            modify_theme_settings_file(settings_ini_path, apply_theme_text)
            ask_restart_option()
        else:
            messagebox.showinfo("Changes not applied")
    else:
        deluge_install_folder = entry_var.get()
        gtk_3_0_folder = os.path.join(deluge_install_folder, FOLDER_SHARE, FOLDER_GTK_3_0)
        if not os.path.exists(gtk_3_0_folder):
            os.makedirs(gtk_3_0_folder)

        apply_theme_text = f"gtk-application-prefer-dark-theme={str(is_dark_apply).lower()}\n"
        modify_theme_settings_file(settings_ini_path, apply_theme_text)
        ask_restart_option()

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

def choose_color(color_display, color_variables, index):
    color = askcolor()[1]
    if color:
        color_display.config(bg=color)
        color_variables[index] = color  # Update the color_variables list with the chosen color

def modify_css_file(css_file_path, new_colors):
    INDEX_SCOPE_OF_MODIFICATION = 5

    # Read the content of the CSS file
    with open(css_file_path, 'r') as file:
        lines = file.readlines()

    # Define the color names and their corresponding new values
    color_names = ['background', 'accent', 'tertiary']

    # Create a dictionary to store color mappings
    color_mapping = {name: color for name, color in zip(color_names, new_colors)}

    # Create a new list of lines with updated colors
    new_lines = []
    for index, line in enumerate(lines):
        updated_line = line  # Initialize the updated line with the original line
        for name, new_color in color_mapping.items():
            if index < INDEX_SCOPE_OF_MODIFICATION and f'@define-color {name}' in line:
                updated_line = f'@define-color {name} {new_color};\n'
        new_lines.append(updated_line)

    # Write the modified content back to the CSS file
    with open(css_file_path, 'w') as file:
        file.writelines(new_lines)

def apply_custom_theme(color_variables):
    settings_ini_path = get_settings_path()
    css_themes_path = get_themes_css_path()

    if os.path.exists(settings_ini_path):
        modify_theme_settings_file(settings_ini_path, "gtk-theme-name=Naster")
        modify_css_file(css_themes_path, color_variables)
        ask_restart_option()

def show_custom_theme_menu():
    subdialog = tk.Toplevel(window)
    subdialog.title("Color Selection")

    # Make the subdialog modal
    subdialog.grab_set()

    # Create a frame for color selection in a horizontal layout
    color_frame = tk.Frame(subdialog)
    color_frame.pack(side="top")

    # Create labels for color selection in the subdialog
    color_labels = ["Background", "Text", "Line selection"]
    color_display_labels = []
    color_variables = ["", "", ""]

    for index, label_text in enumerate(color_labels):
        label = tk.Label(color_frame, text=label_text + " Color:")
        label.pack(side="left", padx=10)

        color_display = tk.Label(color_frame, width=10, height=2)
        color_display.pack(side="left", padx=10)

        color_display_labels.append(color_display)

        choose_button = tk.Button(color_frame, text="Choose Color", command=lambda display=color_display, vars=color_variables, idx=index: choose_color(display, vars, idx))
        choose_button.pack(side="left", padx=10)

    # Create a frame for Apply and Cancel buttons
    button_frame = tk.Frame(subdialog)
    button_frame.pack(side="top", pady=10)

    # Apply button
    apply_button = tk.Button(button_frame, text="Apply", command=lambda: [apply_custom_theme(color_variables), subdialog.destroy()])
    apply_button.pack(side="left", padx=10)

    # Cancel button
    cancel_button = tk.Button(button_frame, text="Cancel", command=subdialog.destroy)
    cancel_button.pack(side="left", padx=10)

    subdialog.protocol("WM_DELETE_WINDOW", subdialog.destroy)  # Allow closing the subdialog

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

# Custom theme button
apply_custom_button = tk.Button(window, text=APPLY_CUSTOM_THEME_BUTTON_TEXT, command=show_custom_theme_menu)
apply_custom_button.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

# Quit button
quit_button = tk.Button(window, text=QUIT_BUTTON_TEXT, command=quit_application)
quit_button.grid(row=4, column=1, padx=20, pady=10)

# Result label
result_label = tk.Label(window, text=RESULT_LABEL_INITIAL_TEXT)
result_label.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

# Start the GUI main loop
window.mainloop()
