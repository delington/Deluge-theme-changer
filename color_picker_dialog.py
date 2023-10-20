import tkinter as tk
from tkinter.colorchooser import askcolor
from theme_processor import apply_custom_theme

def choose_color(color_display, color_variables, index):
    color = askcolor()[1]
    if color:
        color_display.config(bg=color)
        color_variables[index] = color  # Update the color_variables list with the chosen color

def show_custom_theme_menu(root_window):
    subdialog = tk.Toplevel(root_window)
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