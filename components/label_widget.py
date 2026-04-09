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

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def set_text(self, text):
        self.label.config(text=text)
