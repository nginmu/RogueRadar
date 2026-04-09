from components.label_widget import SimpleLabel
from tkinter import ttk

class SecondTab:
    def __init__(self, parent, model):
        self.model = model
        self.frame = ttk.Frame(parent)
        self._build_ui()
        model.register_observer(self)

    def _build_ui(self):
        self.label = SimpleLabel(self.frame, self.model.get("second_tab_text"))
        self.label.pack(padx=20, pady=20)

    def update(self, key, value):
        if key == "second_tab_text":
            self.label.set_text(value)

    def get_frame(self):
        return self.frame
