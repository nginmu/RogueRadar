# This is /components/entry_widget.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk
from tkinter import ttk
from theme import Theme

class SimpleEntry:

    def __init__(self, parent, default_text=""):

        self.var = tk.StringVar(value=default_text)

        self.entry = ttk.Entry(
            parent,
            textvariable=self.var,
            font=Theme.FONT_DEFAULT
        )

    # GEOMETRY MANAGEMENT
    def pack(self, **kwargs):

        self.entry.pack(**kwargs)

    # TEXT ACCESS
    def get_text(self):
        return self.var.get()

    def set_text(self, text):
        self.var.set(text)

# This is the End Of File - /components/entry_widget.py