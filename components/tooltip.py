# This is /components/tooltip.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

import tkinter as tk

class ToolTip:

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def show(self, text, x, y):

        self.hide()

        if not text:
            return

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("TkDefaultFont", 9),
            justify="left",
            wraplength=300,
        )
        label.pack(padx=4, pady=2)

    def hide(self):

        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except Exception:
                pass
            self.tipwindow = None

# This is the End Of File - /components/tooltip.py
