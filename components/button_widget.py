# This is /components/button_widget.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

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

        # STYLING
        style = ttk.Style()
        style.configure(
            "TButton",
            font=Theme.FONT_DEFAULT,
            foreground=Theme.COLOR_BUTTON_FG
        )

    # GEOMETRY MANAGEMENT

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

# This is the End Of File - /components/button_widget.py