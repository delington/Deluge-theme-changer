import os
import psutil
import subprocess
from tkinter import messagebox, StringVar
from shared import entry_var

from constants import (
    FILE_GTK_CSS,
    FILE_SETTINGS_INI,
    FOLDER_GTK_3_0,
    FOLDER_NASTER,
    FOLDER_SHARE,
    FOLDER_THEMES,
    DELUGE_EXECUTABLE
)

def get_GTK_folder_path() -> StringVar:
    deluge_install_folder = entry_var.get()
    return os.path.join(deluge_install_folder, FOLDER_SHARE, FOLDER_GTK_3_0)

def get_settings_path():
    folder_path = get_GTK_folder_path()
    return os.path.join(folder_path, FILE_SETTINGS_INI)

def get_themes_css_path():
    deluge_install_folder = entry_var.get()
    return os.path.join(deluge_install_folder, FOLDER_SHARE, FOLDER_THEMES, FOLDER_NASTER, FOLDER_GTK_3_0, FILE_GTK_CSS)

def modify_theme_settings_file(settings_ini_path, apply_theme_text):
    with open(settings_ini_path, 'w') as settings_ini_file:
        settings_ini_file.write("[Settings]\n")
        settings_ini_file.write(apply_theme_text)

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

def get_deluge_process():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = process.info['name']
            if process_name == 'deluge.exe':
                return psutil.Process(process.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def close_and_restart_deluge(deluge_folder):
    deluge_exe_path = os.path.join(deluge_folder, DELUGE_EXECUTABLE)
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

def apply_custom_theme(color_variables):
    settings_ini_path = get_settings_path()
    css_themes_path = get_themes_css_path()

    if os.path.exists(settings_ini_path):
        modify_theme_settings_file(settings_ini_path, "gtk-theme-name=Naster")
        modify_css_file(css_themes_path, color_variables)
        ask_restart_option()