import tkinter as tk
from tkinter import ttk
from theme import Theme

class SimpleEntry:
    def __init__(self, parent, default_text=""):
        self.var = tk.StringVar(value=default_text)
        self.entry = ttk.Entry(parent, textvariable=self.var, font=Theme.FONT_DEFAULT)

    def pack(self, **kwargs):
        self.entry.pack(**kwargs)

    def get_text(self):
        return self.var.get()

    def set_text(self, text):
        self.var.set(text)
