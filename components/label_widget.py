# This is /components/label_widget.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk
from tkinter import ttk
from theme import Theme

class SimpleLabel:

    def __init__(self, parent, text, font=None, fg=None):

        self.label = ttk.Label(
            parent,
            text=text,
            font=font or Theme.FONT_DEFAULT,
            foreground=fg or Theme.COLOR_LABEL
        )

    # GEOMETRY MANAGEMENT
    def pack(self, **kwargs):

        self.label.pack(**kwargs)

    # CONTENT UPDATE
    def set_text(self, text):

        self.label.config(text=text)

# This is the End Of File - /components/label_widget.py