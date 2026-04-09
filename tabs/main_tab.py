from components.label_widget import SimpleLabel
from components.button_widget import SimpleButton
from tkinter import ttk

class MainTab:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self._build_ui()

    def _build_ui(self):
        self.label = SimpleLabel(self.frame, "Welcome to the Main Tab")
        self.label.pack(padx=20, pady=10)

        self.button = SimpleButton(
            self.frame,
            "Update Second Tab",
            command=self._update_second_tab
        )
        self.button.pack(padx=20, pady=10)

    def _update_second_tab(self):
        self.controller.update_second_tab("Updated via Components Library!")

    def get_frame(self):
        return self.frame
