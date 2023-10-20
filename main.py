import tkinter as tk
from tkinter import filedialog, StringVar
from color_picker_dialog import show_custom_theme_menu
from theme_processor import apply_theme
from shared import entry_var, window

from constants import (
    APPLY_CUSTOM_THEME_BUTTON_TEXT,
    APPLY_DARK_BUTTON_TEXT,
    APPLY_LIGHT_BUTTON_TEXT,
    BROWSE_BUTTON_TEXT,
    FOLDER_LABEL_TEXT,
    QUIT_BUTTON_TEXT,
    RESULT_LABEL_INITIAL_TEXT,
    WINDOW_TITLE,
)

def select_install_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_var.set(folder_selected)

def apply_dark_theme():
    apply_theme(True)

def apply_light_theme():
    apply_theme(False)

def on_custom_theme_apply_button_click():
    show_custom_theme_menu(window)

def quit_application():
    window.quit()

window.title(WINDOW_TITLE)

# Label and entry for folder selection
folder_label = tk.Label(window, text=FOLDER_LABEL_TEXT)
folder_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

folder_entry = tk.Entry(window, textvariable=entry_var, width=40)
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
apply_custom_button = tk.Button(window, text=APPLY_CUSTOM_THEME_BUTTON_TEXT, command=on_custom_theme_apply_button_click)
apply_custom_button.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

# Quit button
quit_button = tk.Button(window, text=QUIT_BUTTON_TEXT, command=quit_application)
quit_button.grid(row=4, column=1, padx=20, pady=10)

# Result label
result_label = tk.Label(window, text=RESULT_LABEL_INITIAL_TEXT)
result_label.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

# Start the GUI main loop
window.mainloop()
