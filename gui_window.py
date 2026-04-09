import tkinter as tk
from tkinter import ttk
from tabs.main_tab import MainTab
from tabs.second_tab import SecondTab
import config
from theme import Theme

class AppWindow:
    def __init__(self, controller, model):
        self.controller = controller
        self.model = model
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.root.configure(bg=Theme.COLOR_BG)
        self._create_tabs()

    def _create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.main_tab = MainTab(self.notebook, self.controller)
        self.second_tab = SecondTab(self.notebook, self.model)

        self.notebook.add(self.main_tab.get_frame(), text=config.TAB_NAMES[0])
        self.notebook.add(self.second_tab.get_frame(), text=config.TAB_NAMES[1])

    def run(self):
        self.root.mainloop()
