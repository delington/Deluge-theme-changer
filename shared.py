import tkinter as tk
import platform
from constants import (
    DELUGE_DEFAULT_PATH
)


def get_entry_var():
    if platform.system() == "Windows":
        return tk.StringVar(value=DELUGE_DEFAULT_PATH)
    
    return tk.StringVar()

# Create the main window
window = tk.Tk()
entry_var = get_entry_var()