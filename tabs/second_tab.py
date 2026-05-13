# This is /tabs/second_tab.py
# RR V3 iteration 001
#
# Written by ChatGPT & Claude
# Steered by Nginmu Mbetse
# May 7 2026

from tkinter import ttk
from components.label_widget import SimpleLabel

class SecondTab:

    def __init__(self, parent, controller):
        self.controller = controller
        self.model = controller.model
        self.frame = ttk.Frame(parent)
        self._build_ui()
        self.model.register_observer(self)

    #UI
    def _build_ui(self):
        self.label = SimpleLabel(
            self.frame,
            self.model.get("second_tab_text")
        )
        self.label.pack(padx=20, pady=20)

    #MODEL
    def update(self, key, value, is_new):
        if key == "second_tab_text":
            self.label.set_text(value)

    #ACCESS
    def get_frame(self):
        return self.frame

# This is the End Of File - /tabs/second_tab.py