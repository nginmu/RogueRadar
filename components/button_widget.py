import tkinter as tk
from tkinter import ttk
from theme import Theme

class SimpleButton:
    def __init__(self, parent, text, command=None):
        self.button = ttk.Button(
            parent,
            text=text,
            command=command
        )
        style = ttk.Style()
        style.configure(
            "TButton",
            font=Theme.FONT_DEFAULT,
            foreground=Theme.COLOR_BUTTON_FG
        )

    def pack(self, **kwargs):
        self.button.pack(**kwargs)
